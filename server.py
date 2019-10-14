from flask import Flask
from flask_mysqldb import MySQL

import config


# endpoint blueprints
from api import artists
from api import genres
from api import keys
from api import songs
from api import stats


# create application instance and set configuration variables

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'webengineering'

mysql = MySQL(app)

# register endpoints
app.register_blueprint(artists.construct_blueprint(mysql))
app.register_blueprint(genres.construct_blueprint(mysql))
app.register_blueprint(keys.construct_blueprint(mysql))
app.register_blueprint(songs.construct_blueprint(mysql))
app.register_blueprint(stats.construct_blueprint(mysql))


# run application if standalone mode
if __name__ == '__main__':
    app.run(config.address, port=config.port, debug=config.debug)
