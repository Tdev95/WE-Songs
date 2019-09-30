from flask import Flask
from api import api
import config

# create application instance and register api

app = Flask(__name__)
app.register_blueprint(api)

# run application if standalone mode
if __name__ == '__main__':
    app.run(config.address, port=config.port, debug=config.debug)
