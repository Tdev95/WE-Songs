from flask import Blueprint, abort, request, Response

import util
import collections
import json


def create_constraints():
    constraints = {
        'threshold': [util.TypeConstraint('int')],
        'year': [util.TypeConstraint('int')]
    }
    return constraints


def create_query(valid_args):
    query = 'SELECT genre, COUNT(*) FROM artist GROUP BY genre '
    if 'threshold' in valid_args:
        query += f'HAVING COUNT(*) >= {valid_args["threshold"]}'
    query += ' ORDER BY COUNT(*) DESC;'
    return query


def format_json(rows):
    list = []
    for row in rows:
        d = collections.OrderedDict()
        d['genre'] = row[0]
        d['count'] = row[1]
        list.append(d)
    return json.dumps(list)


def format_csv(rows):
    delim = ' '
    newline = '\n'
    csv = f'genre count {newline}'
    for row in rows:
        csv += f'"{row[0]}"{delim}{row[1]}{delim}{newline}'
    return csv


def construct_blueprint(connector):
    '''constructs blueprint'''
    blueprint = Blueprint('genres', __name__)

    @blueprint.route('/genres')
    def genres():
        '''
        returns a set of genre:count pairs for a set of songs

        request parameters:
        threshold: integer value describing the minimum number of songs needed for a genre to appear
        '''
        constraints = create_constraints()
        valid_args = util.sanitize(request.args, constraints)
        if valid_args.keys() != set(request.args.keys()):
            abort(400)

        # create query
        query = create_query(valid_args)

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
        except Exception:
            # bad request if query fails
            abort(400)
    return blueprint
