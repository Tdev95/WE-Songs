from flask import Blueprint, abort

from util import execute_query


def construct_blueprint(mysql):
    '''constructs blueprint'''
    blueprint = Blueprint('genres', __name__)

    @blueprint.route('/genres')
    def genres():
        abort(501)
    return blueprint
