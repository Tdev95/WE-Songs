from flask import Flask, render_template
import config
import mysql.connector

# api endpoint blueprints
from api import artists
from api import genres
from api import keys
from api import songs
from api import songs_crud
from api import stats

# create application instance

app = Flask(__name__)

# connect to MySQL database
connection = mysql.connector.Connect(host=config.mysql_host, user=config.mysql_user,
                                     password=config.mysql_password, database=config.mysql_db,
                                     auth_plugin='mysql_native_password')

# register api endpoints
app.register_blueprint(artists.construct_blueprint(connection))
app.register_blueprint(genres.construct_blueprint(connection))
app.register_blueprint(keys.construct_blueprint(connection))
app.register_blueprint(songs.construct_blueprint(connection))
app.register_blueprint(songs_crud.construct_blueprint(connection))
app.register_blueprint(stats.construct_blueprint(connection))


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/artists/home', methods=['GET'])
def artistsHome():
    return render_template('artist.html')

@app.route('/songs/home', methods=['GET'])
def songsHome():
    return render_template('songs.html')

@app.route('/songs/home/songCRUD', methods=['GET'])
def songCRUD():
    return render_template('songCRUD.html')

@app.route('/keys/home', methods=['GET'])
def keysHome():
    return render_template('keys.html')

@app.route('/genres/home', methods=['GET'])
def genresHome():
    return render_template('genres.html')

@app.route('/stats/home', methods=['GET'])
def statsHome():
    return render_template('stats.html')


# run application if standalone mode
if __name__ == '__main__':
    app.run(config.address, port=config.port, debug=config.debug)
