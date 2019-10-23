from flask import Blueprint, request, abort, Response
import collections
import json
import util


def create_get_constraints():
    constraints = {
        'id': [util.TypeConstraint('str'), util.LengthConstraint(18, 18)],
        'genre': [util.TypeConstraint('str')],
        'release': [util.TypeConstraint('int')],
        'artist': [util.TypeConstraint('str'), util.LengthConstraint(18, 18)],
        'year': [util.TypeConstraint('int')],
        'sort': [util.ValueConstraint(['hotness'])],
        'page': [util.TypeConstraint('int')]
    }
    return constraints


def create_get_queries(valid_args):
    # escape ' in genre strings
    if 'genre' in valid_args:
        genre = ''
        for c in valid_args['genre']:
            if(ord(c) == ord("'")):
                genre += "\\"
            genre += c
        valid_args['genre'] = genre

    where_flag = False

    select1 = 'SELECT *'
    select2 = 'SELECT COUNT(*)'
    from1 = 'FROM SONG'
    where = ''

    if 'id' in valid_args:
        if not where_flag:
            where += ' WHERE '
            where_flag = True
        where += 'id = "' + valid_args['id'] + '"'

    if 'artist' in valid_args:
        if not where_flag:
            where += ' WHERE '
            where_flag = True
        else:
            where += ' AND '
        where += f'artist_id = "{valid_args["artist"]}"'

    if 'release' in valid_args:
        if not where_flag:
            where += ' WHERE '
            where_flag = True
        else:
            where += ' AND '
        where += 'release_id = ' + valid_args['release']

    if 'year' in valid_args:
        if not where_flag:
            where += ' WHERE '
            where_flag = True
        else:
            where += ' AND '
        where += 'year = ' + valid_args['year']

    if 'genre' in valid_args:
        if not where_flag:
            where += ' WHERE '
            where_flag = True
        else:
            where += ' AND '
        where += 'artist_id IN (SELECT id AS artist_id FROM artist WHERE genre LIKE "%' + \
            valid_args['genre'] + '%")'

    order = ''
    # popularity
    if 'sort' in valid_args:
        if valid_args['sort'] == 'hotness':
            order += 'ORDER BY hotness'

    # pagination
    page = 1
    group = ''
    if 'page' in valid_args:
        page = int(valid_args['page'])
    group += 'LIMIT 50 offset ' + str((page-1) * 50)

    query1 = f'{select1} {from1} {where} {order} {group};'
    query2 = f'{select2} {from1} {where} {order};'
    return (query1, query2)


def format_json(rows):
    list = []
    for row in rows:
        d = collections.OrderedDict()
        d['id'] = row[0]
        d['artist'] = '/artists?id=' + row[1]
        d['release'] = '/songs?release=' + str(row[2])
        d['artist_mbtags'] = int(row[3])
        d['artists_mbtags_count'] = int(row[4])
        d['bars_confidence'] = row[5]
        d['bars_start'] = row[6]
        d['beats_confidence'] = row[7]
        d['beats_start'] = row[8]
        d['duration'] = row[9]
        d['end_of_fade_in'] = row[10]
        d['hotness'] = row[11]
        d['key_in'] = row[12]
        d['key_confidence'] = row[13]
        d['loudness'] = row[14]
        d['mode'] = row[15]
        d['mode_confidence'] = row[16]
        d['start_of_fade_out'] = row[17]
        d['tatums_confidence'] = row[18]
        d['tatums_start'] = row[19]
        d['tempo'] = row[20]
        d['time_signature'] = row[21]
        d['time_signature_confidence'] = row[22]
        d['title'] = row[23]
        d['year'] = row[24]
        list.append(d)
    return json.dumps(list)


def format_csv(rows):
    delim = ' '
    newline = '\n'
    csv = 'id' + delim
    csv += 'artist' + delim
    csv += 'release' + delim
    csv += 'artist_mbtags' + delim
    csv += 'artists_mbtags_count' + delim
    csv += 'bars_confidence' + delim
    csv += 'bars_start' + delim
    csv += 'beats_confidence' + delim
    csv += 'beats_start' + delim
    csv += 'duration' + delim
    csv += 'end_of_fade_in' + delim
    csv += 'hotness' + delim
    csv += 'key_in' + delim
    csv += 'key_confidence' + delim
    csv += 'loudness' + delim
    csv += 'mode' + delim
    csv += 'mode_confidence' + delim
    csv += 'start_of_fade_out' + delim
    csv += 'tatums_confidence' + delim
    csv += 'tatums_start' + delim
    csv += 'tempo' + delim
    csv += 'time_signature' + delim
    csv += 'time_signature_confidence' + delim
    csv += 'title' + delim
    csv += 'year' + newline
    for row in rows:
        csv += row[0] + delim
        csv += row[1] + delim
        csv += str(row[2]) + delim
        csv += str(int(row[3])) + delim
        csv += str(int(row[4])) + delim
        csv += str(row[5]) + delim
        csv += str(row[6]) + delim
        csv += str(row[7]) + delim
        csv += str(row[8]) + delim
        csv += str(row[9]) + delim
        csv += str(row[10]) + delim
        csv += str(row[11]) + delim
        csv += str(row[12]) + delim
        csv += str(row[13]) + delim
        csv += str(row[14]) + delim
        csv += str(row[15]) + delim
        csv += str(row[16]) + delim
        csv += str(row[17]) + delim
        csv += str(row[18]) + delim
        csv += str(row[19]) + delim
        csv += str(row[20]) + delim
        csv += str(row[21]) + delim
        csv += str(row[22]) + delim
        csv += str(row[23]) + delim
        csv += str(row[24]) + newline
    return csv


def get(connector, request):
    # sanitize input
    constraints = create_get_constraints()
    valid_args = util.sanitize(request.args, constraints)

    # abort if bad request
    if(valid_args.keys() != set(request.args.keys())):
        abort(400)

    # create query
    query, countquery = create_get_queries(valid_args)
    print(query)

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
    except ValueError:
        # bad request if query fails
        abort(400)


def construct_blueprint(connector):
    '''constructs blueprint'''
    blueprint = Blueprint('songs', __name__)

    @blueprint.route('/songs', methods=['GET'])
    def songs():
        '''
        returns a set of songs, providing detailed information about each song

        request parameters:
        id: song ID to filter by
        artist: artist ID to filter by
        release: release ID to filter by
        year: year of release
        genre: (part of) artists genre
        page: page number, each page shows a maximum of 50 results
        '''

        return get(connector, request)
    return blueprint
