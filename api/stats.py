from flask import Blueprint, abort, request, Response

import util
import json
from statistics import mean, median, stdev


def create_constraints():
    constraints = {
        'artist_id': [util.TypeConstraint('str'), util.LengthConstraint(18, 18)],
        'year': [util.TypeConstraint('int'), util.LengthConstraint(1, 5)]
    }
    return constraints


def create_query(valid_args):
    # artist must be in args
    query = f'SELECT hotness FROM song WHERE hotness != -1 AND artist_id = "{valid_args["artist_id"]}"'

    if 'year' in valid_args:
        query += f' AND year = {valid_args["year"]}'
    return query


def format_json(res):
    return json.dumps(res)


def format_csv(res):
    delim = ' '
    newline = '\n'
    csv = 'median' + delim + 'mean' + delim + 'standard deviation' + newline
    csv += res['median'] + delim + res['mean'] + delim + res['standard deviation']
    return csv


def construct_blueprint(connector):
    '''constructs blueprint'''
    blueprint = Blueprint('stats', __name__)

    @blueprint.route('/stats', methods=['GET'])
    def stats():
        '''
         returns a set of median, mean and standard deviation of list of hotnesses of artist_id matching request
        '''
        constraints = create_constraints()
        valid_args = util.sanitize(request.args, constraints)
        # create query
        try:
            query = create_query(valid_args)
        except KeyError:
            abort(400)

        # content negotiation flag
        representation = util.get_representation(request)
        
        # generate response
        try:
            with util.execute_query(connector, query) as rows:
                response = Response()
                # Conventing list of tuples (that contain float) to list of float
                hotness_values = [item for t in rows for item in t]
                if (hotness_values):
                    res = {'median': median(hotness_values),
                           'mean': mean(hotness_values),
                           'standard deviation': stdev(hotness_values)}
                else:
                    # if hotness_values is empty
                    res = {'median': None,
                           'mean': None,
                           'standard deviation': None}

                if representation == 'text/json':
                    response.set_data(format_json(res))
                    response.headers['content-type'] = 'text/json'
                else:
                    response.set_data(format_csv(res))
                    response.headers['content-type'] = 'text/csv'
                response.status = '200'
                return response
        except Exception as ex:
            print(ex)
            # bad request if query fails
            abort(400)

    return blueprint
