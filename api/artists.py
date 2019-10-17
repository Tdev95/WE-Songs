from flask import Blueprint, request, abort, Response, redirect
import collections
import json
import util


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


def construct_blueprint(mysql):
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
        args = request.args

        nc = util.NameConstraint(['id', 'name', 'genre', 'sort', 'page'])
        constraints = {
            'id': [nc, util.TypeConstraint('str'), util.LengthConstraint(18, 18)],
            'name': [nc, util.TypeConstraint('str')],
            'genre': [nc, util.TypeConstraint('str')],
            'sort': [nc, util.ValueConstraint(['hotness', 'familiarity'])],
            'page': [nc, util.TypeConstraint('int')]
        }

        # TODO: add validity checking or risk injection attacks
        valid_args = util.sanitize(args, constraints)

        # if some arguments are invalid, redirect to page with only valid args
        if set(valid_args.keys()) != set(args.keys()):
            # print('warning: invalid args removed')
            url = valid_url(valid_args)
            return redirect(url, code=303)

        # flag used to detect whether WHERE clause was used
        where = False

        # base query
        query = 'SELECT * FROM artist'

        # filter by id, name and/or genre
        if 'id' in valid_args:
            if not where:
                query += ' WHERE '
                where = True
            query += 'id = "' + valid_args['id'] + '"'

        if 'name' in valid_args:
            if not where:
                query += ' WHERE '
                where = True
            else:
                query += ' AND '
            query += 'name LIKE "%' + valid_args['name'] + '%"'

        if 'genre' in valid_args:
            if not where:
                query += ' WHERE '
                where = True
            else:
                query += ' AND '
            query += 'terms LIKE "%' + valid_args['genre'] + '%"'

        # sorting
        if 'sort' in valid_args:
            if valid_args['sort'] == 'hotness':
                query += ' ORDER BY hotttnesss'  # TODO: database spelling
            if valid_args['sort'] == 'familiarity':
                query += ' ORDER BY familiarity'

        # pagination
        page = 1
        if 'page' in valid_args:
            page = int(valid_args['page'])
        query += ' LIMIT 50 offset ' + str((page-1) * 50) + ';'

        # content negotiation flag
        representation = util.get_representation(request)

        # format query result

        try:
            with util.execute_query(mysql, query) as rows:
                response = Response()

                if representation == 'text/json':
                    # format to json
                    list = []
                    for row in rows:
                        d = collections.OrderedDict()
                        d['id'] = row[0]
                        d['familiarity'] = row[1]
                        d['hotness'] = row[2]
                        d['lattitude'] = row[3]
                        d['location'] = row[4]
                        d['longitude'] = row[5]
                        d['name'] = row[6]
                        d['similar'] = row[7]
                        d['terms'] = row[8]
                        d['terms_freq'] = row[9]
                        list.append(d)

                    response.set_data(json.dumps(list))
                    response.headers['content-type'] = 'text/json'
                else:
                    # format to csv
                    delim = ' '
                    newline = '\n'
                    csv = 'id' + delim + 'familiarity' + delim + 'hotness' + delim + 'lattitude' + delim + 'location' + \
                        delim + 'longitude' + delim + 'name' + delim + 'similar' + \
                        delim + 'terms' + delim + 'terms_freq' + newline
                    for row in rows:
                        csv += row[0] + delim  # id
                        csv += str(row[1]) + delim  # familiarity
                        csv += str(row[2]) + delim  # hotness
                        csv += str(row[3]) + delim  # lattitude
                        csv += str(row[4]) + delim  # location
                        csv += str(row[5]) + delim  # longitude
                        csv += '"' + row[6] + '"' + delim  # name
                        csv += str(row[7]) + delim  # similar
                        csv += '"' + row[8] + '"' + delim  # terms
                        csv += str(row[9]) + newline  # terms_freq
                    response.set_data(str(csv))
                    response.headers['content-type'] = 'text/csv'
                response.status = '200'
                # TODO: add header linking any other pages
                return response
        except Exception:
            # bad request if query fails
            abort(400)
    return blueprint
