from flask import Flask, jsonify, render_template
from flask_cors import CORS
import tinder_api

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__, template_folder='assets/')
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/recs/<tinder_token>', methods=['GET'])
def index(tinder_token):
    return render_template('index.html', username=username)

if __name__ == '__main__':
    app.run()