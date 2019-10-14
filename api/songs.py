from flask import Blueprint, request, abort

from util import execute_query


def construct_blueprint(mysql):
    '''constructs blueprint'''
    blueprint = Blueprint('songs', __name__)

    @blueprint.route('/songs', methods=['DELETE', 'GET', 'POST', 'PUT'])
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
    return blueprint
