from flask import Blueprint, abort, request, Response
import collections
import util
import json
import mysql.connector


def get(connector, request, song_id):
    # validate input
    constraints = [util.LengthConstraint(18, 18), util.TypeConstraint('str')]
    valid_args = util.sanitize({'Song': song_id}, constraints)

    if('Song' in valid_args):
        id = valid_args['Song']
    else:
        abort(400)

    query = f'SELECT * FROM song WHERE id = "{id}"'

    # content negotiation flag
    representation = util.get_representation(request)

    # generate response
    try:
        with util.execute_query(connector, query) as rows:
            response = Response()
            if representation == 'text/json':
                response.set_data(format_json(rows[0]))
                response.headers['content-type'] = 'text/json'
            else:
                response.set_data(format_csv(rows[0]))
                response.headers['content-type'] = 'text/csv'
            response.status = '200'
            return response
    except IndexError:
        abort(404)
    except Exception:
        # bad request if query fails
        abort(400)


def format_json(row):
    d = collections.OrderedDict()
    d['id'] = row[0]
    d['artist_id'] = row[1]
    d['release_id'] = str(row[2])
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
    return json.dumps(d)


def delete(connector, request, song_id):
    # validate input
    constraints = [util.LengthConstraint(18, 18), util.TypeConstraint('str')]
    valid_args = util.sanitize({'Song': song_id}, constraints)

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

    # no song was found
    if (rowcount == 0):
        abort(404)

    # format response
    response = Response()
    response.status = '201'
    response.headers['content-type'] = 'text/plain'
    response.set_data(f'Deleted song with id {valid_args["Song"]}')
    return response


def create_song_constraints():
    constraints = {
        'artist_id': [util.TypeConstraint('str'), util.LengthConstraint(18, 18)],
        'release_id': [util.TypeConstraint('int'), util.LengthConstraint(1, 45)],
        'artist_mbtags_count': [util.TypeConstraint('int'), util.LengthConstraint(1, 7)],
        'bars_confidence': [util.TypeConstraint('float'), util.LengthConstraint(1, 20)],
        'bars_start': [util.TypeConstraint('float'), util.LengthConstraint(1, 20)],
        'beats_confidence': [util.TypeConstraint('float'), util.LengthConstraint(1, 20)],
        'beats_start': [util.TypeConstraint('float'), util.LengthConstraint(1, 20)],
        'duration': [util.TypeConstraint('float'), util.LengthConstraint(1, 20)],
        'end_of_fade_in': [util.TypeConstraint('float'), util.LengthConstraint(1, 20)],
        'hotness': [util.TypeConstraint('float'), util.LengthConstraint(1, 20)],
        'key_in': [util.TypeConstraint('int'), util.LengthConstraint(1, 2)],
        'key_confidence': [util.TypeConstraint('float'), util.LengthConstraint(1, 20)],
        'loudness': [util.TypeConstraint('float'), util.LengthConstraint(1, 20)],
        'mode': [util.TypeConstraint('int'), util.LengthConstraint(1, 20)],
        'mode_confidence': [util.TypeConstraint('float'), util.LengthConstraint(1, 20)],
        'start_of_fade_out': [util.TypeConstraint('float'), util.LengthConstraint(1, 20)],
        'tatums_confidence': [util.TypeConstraint('float'), util.LengthConstraint(1, 20)],
        'tatums_start': [util.TypeConstraint('float'), util.LengthConstraint(1, 20)],
        'tempo': [util.TypeConstraint('float'), util.LengthConstraint(1, 20)],
        'time_signature': [util.TypeConstraint('int'), util.LengthConstraint(1, 8)],
        'time_signature_confidence': [util.TypeConstraint('float'), util.LengthConstraint(1, 20)],
        'year': [util.TypeConstraint('int'), util.LengthConstraint(1, 5)]}
    return constraints


def foo(valid_args, name, default):
    # helper function to prevent bloated code
    if(name in valid_args):
        return valid_args[name]
    else:
        return default


def create_post_query(valid_args):
    # make sure all mandatory arguments are present
    mandatory_args = ['id', 'artist_id', 'release_id', 'loudness',
                      'duration', 'key_in', 'mode', 'tempo', 'time_signature']

    for arg in mandatory_args:
        if(arg not in valid_args):
            abort(400)

    # create tuple with query args
    tuple = ()
    tuple += (valid_args['id'],)
    tuple += (valid_args['artist_id'],)
    tuple += (valid_args['release_id'],)
    tuple += (0,)  # artist_mbtags
    tuple += (foo(valid_args, 'artist_mbtags_count', 0),)
    tuple += (foo(valid_args, 'bars_confidence', 0),)
    tuple += (foo(valid_args, 'bars_start', 0),)
    tuple += (foo(valid_args, 'beats_confidence', 0),)
    tuple += (foo(valid_args, 'beats_start', 0),)
    tuple += (valid_args['duration'],)
    tuple += (foo(valid_args, 'end_of_fade_in', 0),)
    tuple += (foo(valid_args, 'hotness', 0),)
    tuple += (valid_args['key_in'],)
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
        args = json.loads(request.data)
        constraints = create_song_constraints()
        valid_args = util.sanitize(args, constraints)
        query = create_post_query(valid_args)

        # execute query
        cursor = connector.cursor()
        cursor.execute(query)
        connector.commit()
        rowcount = cursor.rowcount

        # format response
        response = Response()
        response.status = '201'
        response.headers['content-type'] = 'text/plain'
        response.set_data(f'Added song with id {valid_args["id"]}')
        return response
    except mysql.connector.IntegrityError:
        # song already in database
        abort(409)
    except Exception:
        # bad request if anything fails
        abort(400)


def create_patch_query(id, valid_args):

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


def patch(connector, request, song_id):
    try:
        # validate song id
        print("here11")
        song_constraint = [util.LengthConstraint(18, 18), util.TypeConstraint('str')]
        valid = util.sanitize({'Song': song_id}, song_constraint)
        if('Song' in valid):
            id = valid['Song']
        else:
            abort(400)

        # validate json and execute query
        args = json.loads(request.data)
        constraints = create_song_constraints()
        valid_args = util.sanitize(args, constraints)
        query = create_patch_query(id, valid_args)

        # not using util.execute_query in order to obtain rowcount
        cursor = connector.cursor()
        cursor.execute(query)
        connector.commit()
        rowcount = cursor.rowcount

        # no song was found
        if (rowcount == 0):
            abort(404)

        # format response
        response = Response()
        response.status = '200'
        response.set_data(f'Modified song with id {valid_args["id"]}')
        return response
    except ValueError:
        # bad request if anything fails
        abort(400)


def construct_blueprint(connector):
    '''constructs blueprint'''
    blueprint = Blueprint('songs_cud', __name__)

    @blueprint.route('/songs/<song_id>', methods=['GET', 'DELETE', 'POST', 'PATCH'])
    def songs(song_id):
        if request.method == 'GET':
            return get(connector, request, song_id)
        elif request.method == 'DELETE':
            return delete(connector, request, song_id)
        elif request.method == 'POST':
            return post(connector, request)
        elif request.method == 'PATCH':
            return patch(connector, request, song_id)
    return blueprint
