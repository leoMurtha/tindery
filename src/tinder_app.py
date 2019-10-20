from flask import Flask, jsonify, render_template
from flask_cors import CORS
import tinder_api
from random import random

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__, template_folder='assets/')
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/', methods=['GET'])
def show_rec():
    return render_template('index.html', random=random())

@app.route('/SomeFunction')
def SomeFunction():
    print('In SomeFunction')
    return str(random())

if __name__ == '__main__':
    app.run()