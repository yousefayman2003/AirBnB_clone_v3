#!/usr/bin/python3
'''lsadfkjlkadsjf lksadj k jsdalfk jdaskl fljadsfkl.'''
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown(exception):
    """Close the current storage session."""
    storage.close()


@app.errorhandler(404)
def handle_not_found_error(e):
    "handles not found error"
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.register_blueprint(app_views, url_prefix='/api/v1')
    app.run(host=host, port=port, threaded=True)
