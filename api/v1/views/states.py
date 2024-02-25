#!/usr/bin/python3
"""Module for handling state-related API endpoints."""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def states():
    """get all states"""
    states = [obj.to_dict() for obj in storage.all("State").values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def state(state_id):
    """get state"""
    states = storage.all("State").values()
    state = [obj.to_dict() for obj in states if obj.id == state_id]
    if state == []:
        abort(404)
    return jsonify(state[0])


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_state(state_id):
    """delete a state"""
    states = storage.all("State").values()
    state = [obj.to_dict() for obj in states if obj.id == state_id]
    if state == []:
        abort(404)
    state.remove(state[0])
    for obj in states:
        if obj.id == state_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/states/', strict_slashes=False, methods=['POST'])
def crt_state():
    """create state"""
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


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def updtstate(state_id):
    """update a state"""
    states = storage.all("State").values()
    state = [obj.to_dict() for obj in states if obj.id == state_id]
    if state == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    state[0]['name'] = request.json['name']
    for obj in states:
        if obj.id == state_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(state[0]), 200
