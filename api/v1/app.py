#!/usr/bin/python3
'''lsadfkjlkadsjf lksadj k jsdalfk jdaskl fljadsfkl.'''
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """Close the current storage session."""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    '''return render_template'''
    return jsonify(error='Not found'), 404)

if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.register_blueprint(app_views, url_prefix='/api/v1')
    app.url_map.strict_slashes = False
    app.run(host=host, port=port, threaded=True)
