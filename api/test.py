from flask import Blueprint

from util import execute_query


def construct_blueprint(mysql):
    '''constructs blueprint'''
    blueprint = Blueprint('test', __name__)

    @blueprint.route('/test/', methods=['GET', 'POST'])
    def test():
        with execute_query(mysql, 'SELECT * FROM artist;') as rv:
            print(rv)
            return str(rv)
    return blueprint
