from flask import Flask
from api import construct_blueprint
import config
from flask_mysqldb import MySQL


# create application instance and register api

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'webengineering'

mysql = MySQL(app)
app.register_blueprint(construct_blueprint(mysql))


# run application if standalone mode
if __name__ == '__main__':
    app.run(config.address, port=config.port, debug=config.debug)
