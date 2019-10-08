from flask import Flask
from api import api
import config
from flask_mysqldb import MySQL


# create application instance and register api

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'MyDB'
app.register_blueprint(api)
mysql = MySQL(app)


@app.route('/sql/', methods=['GET', 'POST'])
def sql():
    cur = mysql.connection.cursor()
    cur.execute
    mysql.connection.commit("INSERT INTO MyUsers(firstName, lastName) VALUES (X, Y)")
    cur.close()
    return 'success'


# run application if standalone mode
if __name__ == '__main__':
    app.run(config.address, port=config.port, debug=config.debug)
