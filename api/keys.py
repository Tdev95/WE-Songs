from flask import Blueprint, abort, request, Response

import util
import json
import collections


def create_constraints():
    def threshold_check(name, input):
        try:
            value = float(input)
        except Exception:
            return False
        return value >= 0 and value <= 1

    constraints = {
        'genre': [util.TypeConstraint('str'), util.LengthConstraint(1, 100)],
        'hotnessThreshold': [util.TypeConstraint('float'), util.CustomConstraint(threshold_check),
                             util.LengthConstraint(1, 20)]
    }
    return constraints


def create_query(valid_args):
    query = 'SELECT key_in, COUNT(*)'
    where = False

    if 'genre' in valid_args:
        query += ' FROM song JOIN artist ON song.artist_id = artist.id'
        query += f' WHERE genre LIKE "%{valid_args["genre"]}%"'
        where = True
    else:
        query += ' FROM song'

    if 'hotnessThreshold' in valid_args:
        if where is False:
            query += ' WHERE'
        else:
            query += ' AND'
        query += f' song.hotness >= {valid_args["hotnessThreshold"]}'
    query += ' GROUP BY key_in ORDER BY key_in'
    return query


def format_json(rows):
    list = []
    for row in rows:
        d = collections.OrderedDict()
        d['key'] = int(row[0])
        d['count'] = row[1]
        list.append(d)
    return json.dumps(list)


def format_csv(rows):
    delim = ' '
    newline = '\n'
    csv = f'key{delim}count{newline}'
    for row in rows:
        csv += f'{str(int(row[0]))}{delim}{row[1]}{newline}'
    return csv


def construct_blueprint(connector):
    '''constructs blueprint'''
    blueprint = Blueprint('keys', __name__)

    @blueprint.route('/keys')
    def keys():
        '''
        returns a set of key:count pairs for a set of songs

        request parameters:
        genre: (part of) a string describing the genre
        threshold: value between 0 and 1 as the lower limit for the popularity of songs
        '''
        constraints = create_constraints()
        valid_args = util.sanitize(request.args, constraints)

        if(valid_args.keys() != set(request.args.keys())):
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
