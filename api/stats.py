from flask import Blueprint, abort

from util import execute_query


def construct_blueprint(connector):
    '''constructs blueprint'''
    blueprint = Blueprint('stats', __name__)

    @blueprint.route('/stats', methods=['GET'])
    def stats():
        abort(501)

    return blueprint
