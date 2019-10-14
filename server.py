from flask import Flask, render_template
from flask_mysqldb import MySQL

import config


# api endpoint blueprints
from api import artists
from api import genres
from api import keys
from api import songs
from api import stats


# create application instance and set configuration variables

app = Flask(__name__)
app.config['MYSQL_HOST'] = config.mysql_host
app.config['MYSQL_USER'] = config.mysql_user
app.config['MYSQL_PASSWORD'] = config.mysql_password
app.config['MYSQL_DB'] = config.mysql_db

mysql = MySQL(app)

# register api endpoints
app.register_blueprint(artists.construct_blueprint(mysql))
app.register_blueprint(genres.construct_blueprint(mysql))
app.register_blueprint(keys.construct_blueprint(mysql))
app.register_blueprint(songs.construct_blueprint(mysql))
app.register_blueprint(stats.construct_blueprint(mysql))


@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')


# run application if standalone mode
if __name__ == '__main__':
    app.run(config.address, port=config.port, debug=config.debug)
