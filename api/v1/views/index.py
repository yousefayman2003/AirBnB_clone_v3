#!/usr/bin/python3
'''sadkljf;ldsjaf ksaldjflk asdlfkj lksdajf ;lsad.'''
from api.v1.views import app_views
from flask import jsonify
import models
from models import storage
from models.base_model import BaseModel


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def get_status():
    '''dsajlfjlkadsfjlksdaj flkjsd lkfjasldk fkasjd.'''
    return jsonify({"status": "OK"})


@app_views.route('stats', strict_slashes=False, methods=['GET'])
def stats():
    '''responses'''
    todos = {'states': 'State', 'users': 'User',
             'amenities': 'Amenity', 'cities': 'City',
             'places': 'Place', 'reviews': 'Review'}

    for key in todos:
        todos[key] = storage.count(todos[key])
    return jsonify(todos)
