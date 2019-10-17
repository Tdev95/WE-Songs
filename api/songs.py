from flask import Blueprint, request, abort, Response
import collections
import json
import util


def create_query(valid_args):

    where = False

    query = 'SELECT * FROM song'

    if 'id' in valid_args:
        if not where:
            query += ' WHERE '
            where = True
        query += 'id = "' + valid_args['id'] + '"'

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


def construct_blueprint(mysql):
    '''constructs blueprint'''
    blueprint = Blueprint('songs', __name__)

    @blueprint.route('/songs', methods=['DELETE', 'GET', 'POST', 'PUT'])
    def songs():
        if request.method == 'DELETE':
            abort(501)
        elif request.method == 'GET':
            # sanitize input
            nc = util.NameConstraint(['id', 'genre', 'release', 'artist', 'year', 'page'])
            constraints = {
                'id': [nc],
                'genre': [nc],
                'release': [nc],
                'artist': [nc],
                'year': [nc],
                'page': [nc]
            }
            valid_args = util.sanitize(request.args, constraints)
            # abort if bad request
            if(valid_args.keys() != set(request.args.keys())):
                abort(400)

            # create query
            query = create_query(valid_args)

            # content negotiation flag
            representation = util.get_representation(request)
            try:
                with util.execute_query(mysql, query) as rows:
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
            abort(501)
        elif request.method == 'POST':
            # is json
            print(request.is_json)
            abort(501)
        elif request.method == 'PUT':
            abort(501)
    return blueprint
