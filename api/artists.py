from flask import Blueprint, request, abort, Response, redirect
import collections
import json
import util


def create_constraints():
    constraints = {
        'id': [util.TypeConstraint('str'), util.LengthConstraint(18, 18)],
        'name': [util.TypeConstraint('str'), util.LengthConstraint(1, 100)],
        'genre': [util.TypeConstraint('str'), util.LengthConstraint(1, 100)],
        'sort': [util.ValueConstraint(['hotness', 'familiarity'])],
        'page': [util.TypeConstraint('int'), util.LengthConstraint(1, 10)]
    }
    return constraints


def create_queries(valid_args):
    # escape ' in genre strings
    if 'genre' in valid_args:
        genre = ''
        for c in valid_args['genre']:
            if(ord(c) == ord("'")):
                genre += '\\'
            genre += c
        valid_args['genre'] = genre

    # flag used to detect whether WHERE clause was used
    where_flag = False

    # base query
    select1 = 'SELECT *'
    select2 = 'SELECT COUNT(*)'
    from1 = 'FROM artist'

    where = ''

    # filter by id, name and/or genre
    if 'id' in valid_args:
        if not where_flag:
            where += ' WHERE '
            where_flag = True
        where += 'id = "' + valid_args['id'] + '"'

    if 'name' in valid_args:
        if not where_flag:
            where += ' WHERE '
            where_flag = True
        else:
            where += ' AND '
        where += 'name LIKE "%' + valid_args['name'] + '%"'

    if 'genre' in valid_args:
        if not where_flag:
            where += ' WHERE '
            where_flag = True
        else:
            where += ' AND '
        where += 'genre LIKE "%' + valid_args['genre'] + '%"'

    # sorting
    order = ''
    if 'sort' in valid_args:
        if valid_args['sort'] == 'hotness':
            order += ' ORDER BY hotness'  # TODO: database spelling
        if valid_args['sort'] == 'familiarity':
            order += ' ORDER BY familiarity'

    # pagination
    group = ''
    page = 1
    if 'page' in valid_args:
        page = int(valid_args['page'])
    group += ' LIMIT 50 offset ' + str((page-1) * 50) + ';'

    query1 = f'{select1} {from1} {where} {order} {group};'
    query2 = f'{select2} {from1} {where} {order}'
    return (query1, query2)


def valid_url(valid_args):
    '''builds a valid url given a set of valid arguments'''
    url = ''
    if 'id' in valid_args:
        url += 'id=' + valid_args['id'] + '&'
    if 'name' in valid_args:
        url += 'name=' + valid_args['name'] + '&'
    if 'genre' in valid_args:
        url += 'genre=' + valid_args['genre'] + '&'
    if 'sort' in valid_args:
        url += 'sort=' + valid_args['sort'] + '&'
    if 'page' in valid_args:
        url += 'page=' + valid_args['page'] + '&'
    if url != '':
        url = '?' + url[0:(len(url)-1)]
    url = '/artists' + url
    return url


def format_json(rows):
    # format to json
    list = []
    for row in rows:
        d = collections.OrderedDict()
        d['id'] = row[0]
        d['songs'] = f'/songs?artist={row[0]}'
        d['familiarity'] = row[1]
        d['hotness'] = row[2]
        d['lattitude'] = row[3]
        d['location'] = row[4]
        d['longitude'] = row[5]
        d['name'] = row[6]
        d['similar'] = row[7]
        d['genre'] = row[8]
        d['genre_freq'] = row[9]
        list.append(d)

    return json.dumps(list)


def format_csv(rows):
    # format to csv
    delim = ' '
    newline = '\n'
    csv = f'id{delim}songs{delim}familiarity{delim}hotness{delim}lattitude{delim}location' + \
        '{delim}longitude{delim}name{delim}similar' + \
        '{delim}genre{delim}genre_freq{newline}'
    for row in rows:
        csv += row[0] + delim  # id
        csv += f'/songs?artist={row[0]}' + delim  # songs of artist
        csv += str(row[1]) + delim  # familiarity
        csv += str(row[2]) + delim  # hotness
        csv += str(row[3]) + delim  # lattitude
        csv += str(row[4]) + delim  # location
        csv += str(row[5]) + delim  # longitude
        csv += f'"{row[6]}"{delim}'  # name
        csv += str(row[7]) + delim  # similar
        csv += f'"{row[8]}"{delim}'  # genre
        csv += str(row[9]) + newline  # genre_freq
    return csv


def construct_blueprint(connector):
    '''constructs blueprint'''
    blueprint = Blueprint('artists', __name__)

    @blueprint.route('/artists', methods=['GET'])
    def artists():
        '''
        returns a set of artists, providing detailed information about each artist

        request parameters:
        id: artist ID
        name: (part of) artist's name
        genre: (part of) artists genre
        sort: sort by either artist hotness or familiarity
        page: page number, each page shows a maximum of 50 results
        '''

        constraints = create_constraints()

        valid_args = util.sanitize(request.args, constraints)

        # if some arguments are invalid, redirect to page with only valid args
        if set(valid_args.keys()) != set(request.args.keys()):
            # print('warning: invalid args removed')
            url = valid_url(valid_args)
            return redirect(url, code=303)

        # create query
        query, countquery = create_queries(valid_args)

        # content negotiation flag
        representation = util.get_representation(request)

        response = Response()
        # get # of rows
        try:
            with util.execute_query(connector, countquery) as count:
                rows = count[0][0]
                pages = rows/50 + 1

                url = '/artists?'
                for arg in valid_args:
                    if arg != 'page':
                        url += f'{arg}={valid_args[arg]}&'

                # figure out current page
                if('page' in valid_args):
                    page = int(valid_args['page'])
                else:
                    page = 1

                # add links to previous, next page depending on page and pages
                if page > 1:
                    response.headers['Page-Previous'] = url + f'page={page-1}'
                if page < pages:
                    response.headers['Page-Next'] = url + f'page={page+1}'
        except Exception:
            # bad request if query fails
            abort(400)

        # generate response
        try:
            with util.execute_query(connector, query) as rows:

                if representation == 'text/json':
                    response.set_data(format_json(rows))
                    response.headers['content-type'] = 'text/json'
                else:
                    response.set_data(format_csv(rows))
                    response.headers['content-type'] = 'text/csv'
                response.status = '200'
                return response
        except Exception:
            # bad request if query fails
            abort(400)
    return blueprint
