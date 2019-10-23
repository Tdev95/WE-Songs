from flask import Blueprint, abort, request, Response

import util
import json


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

    # format response
    response = Response()
    response.status = '200'
    response.headers['content-type'] = 'text/plain'
    response.set_data(f'Deleted {rowcount} song(s)')
    return response


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
        song_constraint = [util.LengthConstraint(18, 18), util.TypeConstraint('str')]
        valid = util.sanitize({'Song': song_id}, song_constraint)
        if('Song' in valid):
            id = valid['Song']
        else:
            abort(400)
        # validate json and execute query
        args = json.loads(request.json)
        constraints = create_song_constraints()
        valid_args = util.sanitize(args, constraints)
        query = create_patch_query(id, valid_args)

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
    blueprint = Blueprint('songs_cud', __name__)

    @blueprint.route('/songs/<song_id>', methods=['DELETE', 'POST', 'PATCH'])
    def songs(song_id):
        if request.method == 'DELETE':
            return delete(connector, request, song_id)
        elif request.method == 'POST':
            return post(connector, request)
        elif request.method == 'PATCH':
            return patch(connector, request, song_id)
    return blueprint
