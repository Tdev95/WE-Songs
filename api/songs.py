from flask import Blueprint, request, abort, Response
import collections
import json
import util


def create_get_constraints():
    nc = util.NameConstraint(['id', 'genre', 'release', 'artist', 'year', 'sort', 'page'])
    constraints = {
        'id': [nc, util.TypeConstraint('str'), util.LengthConstraint(18, 18)],
        'genre': [nc, util.TypeConstraint('str')],
        'release': [nc, util.TypeConstraint('int')],
        'artist': [nc, util.TypeConstraint('str'), util.LengthConstraint(18, 18)],
        'year': [nc, util.TypeConstraint('int')],
        'sort': [nc, util.ValueConstraint(['hotness'])],
        'page': [nc, util.TypeConstraint('int')]
    }
    return constraints


def create_get_query(valid_args):

    where = False

    query = 'SELECT * FROM song'

    if 'id' in valid_args:
        if not where:
            query += ' WHERE '
            where = True
        query += 'id = "' + valid_args['id'] + '"'

    if 'artist' in valid_args:
        if not where:
            query += ' WHERE '
            where = True
        else:
            query += ' AND '
        query += f'artist_id = "{valid_args["artist"]}"'

    if 'release' in valid_args:
        if not where:
            query += ' WHERE '
            where = True
        else:
            query += ' AND '
        query += 'release_id = ' + valid_args['release']

    if 'year' in valid_args:
        if not where:
            query += ' WHERE '
            where = True
        else:
            query += ' AND '
        query += 'year = ' + valid_args['year']

    if 'genre' in valid_args:
        if not where:
            query += ' WHERE '
            where = True
        else:
            query += ' AND '
        query += 'artist_id IN (SELECT id AS artist_id FROM artist WHERE terms LIKE "%' + \
            valid_args['genre'] + '%")'

    # popularity
    if 'sort' in valid_args:
        if valid_args['sort'] == 'hotness':
            query += ' ORDER BY hotttnesss'  # TODO: database spelling

    # pagination
    page = 1
    if 'page' in valid_args:
        page = int(valid_args['page'])
    query += ' LIMIT 50 offset ' + str((page-1) * 50) + ';'

    return query


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
    query = create_get_query(valid_args)

    # content negotiation flag
    representation = util.get_representation(request)

    # generate response
    try:
        with util.execute_query(connector, query) as rows:
            response = Response()

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


def create_post_constraints():
    return []


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
        constraints = create_post_constraints()
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
        return "test"
    except Exception:
        # bad request if anything fails
        abort(400)


def construct_blueprint(connector):
    '''constructs blueprint'''
    blueprint = Blueprint('songs', __name__)

    @blueprint.route('/songs', methods=['DELETE', 'GET', 'POST', 'PUT'])
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
        elif request.method == 'PUT':
            abort(501)
    return blueprint
