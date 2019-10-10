from flask import Blueprint, request, abort, Response

# create blueprint


def construct_blueprint(mysql):
    api = Blueprint('api', __name__)

    @api.route('/test/', methods=['GET', 'POST'])
    def sql():
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM artist;')
        mysql.connection.commit()
        rv = cur.fetchall()
        cur.close()
        return str(rv)

    @api.route('/artists', methods=['GET'])
    def artists():
        # print URL arguments
        print(request.args)

        # print available arguments
        args = request.args

        header_exists = {
            'id': 'id' in args,
            'genre': 'genre' in args,
            'sort': 'sort' in args,
            'pageSize': 'pageSize' in args,
            'pageStartIndex': 'pageStartIndex' in args
        }

        print(header_exists)

        # print supported mimetypes for content negotiation
        print(request.accept_mimetypes)
        abort(501)

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
