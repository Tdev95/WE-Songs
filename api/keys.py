from flask import Blueprint, abort

from util import execute_query


def construct_blueprint(mysql):
    '''constructs blueprint'''
    blueprint = Blueprint('keys', __name__)

    @blueprint.route('/keys')
    def keys():
        abort(501)

    return blueprint
