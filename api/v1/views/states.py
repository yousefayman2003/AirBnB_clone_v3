#!/usr/bin/python3
"""Module for handling state-related API endpoints."""
import uuid
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from datetime import datetime


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def list_all_states():
    """Retrieve a list of all State objects."""
    states_list = [obj.to_dict() for obj in storage.all("State").values()]
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_single_state(state_id):
    """Retrieve a single State object."""
    all_states = storage.all("State").values()
    state_obj = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if state_obj == []:
        abort(404)
    return jsonify(state_obj[0])


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_single_state(state_id):
    """Delete a single State object."""
    all_states = storage.all("State").values()
    state_obj = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if state_obj == []:
        abort(404)
    state_obj.remove(state_obj[0])
    for obj in all_states:
        if obj.id == state_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'])
def create_single_state():
    """Create a new State object."""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    states = []
    new_state = State(name=request.json['name'])
    storage.new(new_state)
    storage.save()
    states.append(new_state.to_dict())
    return jsonify(states[0]), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_single_state(state_id):
    """Update a single State object."""
    all_states = storage.all("State").values()
    state_obj = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if state_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    state_obj[0]['name'] = request.json['name']
    for obj in all_states:
        if obj.id == state_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(state_obj[0]), 200
