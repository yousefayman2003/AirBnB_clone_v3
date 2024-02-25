#!/usr/bin/python3
'''sadkljf;ldsjaf ksaldjflk asdlfkj lksdajf ;lsad.'''
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def get_status():
    '''dsajlfjlkadsfjlksdaj flkjsd lkfjasldk fkasjd.'''
    return jsonify({"status": "OK"})
