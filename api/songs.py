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


def delete(connector, request):
    # validate input
    if('Song' in request.headers):
        constraints = [util.LengthConstraint(18, 18), util.TypeConstraint('str')]
        valid_args = util.sanitize({'Song': request.headers['Song']}, constraints)
    else:
        abort(400)

    if('Song' in valid_args):
        id = valid_args['Song']
    else:
        abort(400)

    query = f'DELETE FROM song WHERE id = "{id}"'

    # not using util.execute_query in order to obtain rowcount
    try:
        cursor = connector.cursor()
        cursor.execute(query)
        connector.commit()
        rowcount = cursor.rowcount
    except Exception:
        # bad request if query fails
        abort(400)

    # format response
    response = Response()
    response.status = '200'
    response.headers['content-type'] = 'text/plain'
    response.set_data(f'Deleted {rowcount} song(s)')
    return response


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


def create_song_constraints():
    constraints = {
        'artist_id': [util.TypeConstraint('str'), util.LengthConstraint(18, 18)],
        'release_id': [util.TypeConstraint('int')],
        'artist_mbtags_count': [util.TypeConstraint('int')],
        'bars_confidence': [util.TypeConstraint('float')],
        'bars_start': [util.TypeConstraint('float')],
        'beats_confidence': [util.TypeConstraint('float')],
        'beats_start': [util.TypeConstraint('float')],
        'duration': [util.TypeConstraint('float')],
        'end_of_fade_in': [util.TypeConstraint('float')],
        'hotness': [util.TypeConstraint('float')],
        'key_in': [util.TypeConstraint('int')],
        'key_confidence': [util.TypeConstraint('float')],
        'loudness': [util.TypeConstraint('float')],
        'mode': [util.TypeConstraint('int')],
        'mode_confidence': [util.TypeConstraint('float')],
        'start_of_fade_out': [util.TypeConstraint('float')],
        'tatums_confidence': [util.TypeConstraint('float')],
        'tatums_start': [util.TypeConstraint('float')],
        'tempo': [util.TypeConstraint('float')],
        'time_signature': [util.TypeConstraint('int')],
        'time_signature_confidence': [util.TypeConstraint('float')],
        'year': [util.TypeConstraint('int')]}
    return constraints


def foo(valid_args, name, default):
    # helper function to prevent bloated code
    if(name in valid_args):
        return valid_args[name]
    else:
        return default


def create_post_query(valid_args):
    # make sure all mandatory arguments are present
    mandatory_args = ['song_id', 'artist_id', 'release_id', 'loudness',
                      'duration', 'key', 'mode', 'tempo', 'time_signature']
    for arg in mandatory_args:
        if(arg not in valid_args):
            abort(400)

    # create tuple with query args
    tuple = ()
    tuple += (valid_args['song_id'],)
    tuple += (valid_args['artist_id'],)
    tuple += (valid_args['release_id'],)
    tuple += (valid_args['release_id'],)
    tuple += (0,)  # artist_mbtags

    tuple += (foo(valid_args, 'artist_mbtags_count', 0),)

    tuple += (foo(valid_args, 'bars_confidence', 0),)
    tuple += (foo(valid_args, 'bars_start', 0),)
    tuple += (foo(valid_args, 'beats_confidence', 0),)
    tuple += (valid_args['duration'],)
    tuple += (foo(valid_args, 'end_of_fade_in', 0),)
    tuple += (foo(valid_args, 'hotness', 0),)
    tuple += (valid_args['key'],)
    tuple += (foo(valid_args, 'key_confidence', 1),)
    tuple += (valid_args['loudness'],)
    tuple += (valid_args['mode'],)
    tuple += (foo(valid_args, 'mode_confidence', 1),)
    tuple += (foo(valid_args, 'start_of_fade_out', valid_args['duration']),)
    tuple += (foo(valid_args, 'tatums_confidence', 0),)
    tuple += (foo(valid_args, 'tatums_start', 0),)
    tuple += (valid_args['tempo'],)
    tuple += (valid_args['time_signature'],)
    tuple += (foo(valid_args, 'time_signature_confidence', 1),)
    tuple += (0,)  # title
    tuple += (foo(valid_args, 'year', 0),)

    return f'INSERT INTO song VALUES {str(tuple)}'


def post(connector, request):
    try:
        args = json.loads(request.json)
        constraints = create_song_constraints()
        valid_args = util.sanitize(args, constraints)
        query = create_post_query(valid_args)

        # execute query and obtain # rows changed
        cursor = connector.cursor()
        cursor.execute(query)
        connector.commit()
        rowcount = cursor.rowcount

        # format response
        response = Response()
        response.status = '200'
        response.headers['content-type'] = 'text/plain'
        response.set_data(f'Added {rowcount} song(s)')
        return response
    except Exception:
        # bad request if anything fails
        abort(400)


def create_patch_query(valid_args):
    # look for id of song to patch
    id = ''
    if('song_id' in valid_args):
        id = valid_args['song_id']
    else:
        abort(400)

    column_names = ['artist_id', 'release_id', 'artist_mbtags_count',
                    'bars_confidence', 'bars_start', 'beats_confidence', 'beats_start', 'duration',
                    'end_of_fade_in', 'hotness', 'key_in', 'key_confidence', 'loudness', 'mode',
                    'mode_confidence', 'start_of_fade_out', 'tatums_confidence', 'tatums_start',
                    'tempo', 'time_signature', 'time_signature_confidence', 'year']

    # create query
    query = f'UPDATE song SET id = "{id}" '
    for arg in valid_args:
        if(arg in column_names):
            if arg == 'artist_id':
                query += f', {arg} = "{valid_args[arg]}" '
            else:
                query += f', {arg} = {valid_args[arg]} '
    query += f'WHERE id = "{id}"'

    # return query
    return query


def patch(connector, request):
    try:
        args = json.loads(request.json)
        constraints = create_song_constraints()
        valid_args = util.sanitize(args, constraints)
        query = create_patch_query(valid_args)

        # execute query
        cursor = connector.cursor()
        cursor.execute(query)
        connector.commit()

        # format response
        response = Response()
        response.status = '204'
        return response
    except Exception:
        # bad request if anything fails
        abort(400)


def construct_blueprint(connector):
    '''constructs blueprint'''
    blueprint = Blueprint('songs', __name__)

    @blueprint.route('/songs', methods=['DELETE', 'GET', 'POST', 'PATCH'])
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

        if request.method == 'DELETE':
            return delete(connector, request)
        elif request.method == 'GET':
            return get(connector, request)
        elif request.method == 'POST':
            return post(connector, request)
        elif request.method == 'PATCH':
            return patch(connector, request)
    return blueprint
