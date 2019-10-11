from flask import Blueprint, request, abort, Response
from contextlib import contextmanager
import collections
import json


@contextmanager
def execute_query(db, query):
    '''query context manager'''
    cursor = db.connection.cursor()
    cursor.execute(query)
    db.connection.commit()
    yield cursor.fetchall()
    cursor.close()


def construct_blueprint(mysql):
    '''constructs blueprint'''
    api = Blueprint('api', __name__)

    @api.route('/test/', methods=['GET', 'POST'])
    def sql():
        # print URL arguments
        print(request.args)

        # print supported mimetypes for content negotiation
        print(request.accept_mimetypes)

        with execute_query(mysql, 'SELECT * FROM artist;') as rv:
            print(rv)
            return str(rv)

    @api.route('/artists', methods=['GET'])
    def artists():
        '''
        id
        name
        genre
        sort
        page
        '''
        args = request.args

        valid_args = args  # TODO: add validity checking or risk injection attacks

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
        if 'page' in valid_args:
            query += ' LIMIT 50 offset ' + str((int(valid_args['page'])-1) * 50) + ';'
        else:
            query += ' LIMIT 50 offset 0;'

        # content negotiation flag
        mimetypes = request.accept_mimetypes

        representation = 'text/json'
        if ('text/json' not in mimetypes) and ('text/csv' in mimetypes):
            representation = 'text/csv'

        # format query result

        try:
            with execute_query(mysql, query) as rows:
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
                return response
        except ValueError:
            # bad request if query fails
            abort(400)

    @api.route('/songs', methods=['DELETE', 'GET', 'POST', 'PUT'])
    def songs():
        if request.method == 'DELETE':
            abort(501)
        elif request.method == 'GET':
            abort(501)
        elif request.method == 'POST':
            # is json
            print(request.is_json)
            abort(501)
        elif request.method == 'PUT':
            abort(501)

    @api.route('/stats', methods=['GET'])
    def stats():
        response = Response("test data")
        response.status = '501'
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    return api
