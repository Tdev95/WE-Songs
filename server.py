from flask import Flask
import config

# create application instance

app = Flask(__name__)

# routing


@app.route('/hello/')
def home():
    return 'Hello world!'


# run application if standalone mode
if __name__ == '__main__':
    app.run(config.address, port=config.port, debug=config.debug)
