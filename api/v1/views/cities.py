#!/usr/bin/python3
"""cities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def list_cities_of_state(state_id):
    """return a list of all City objects"""
    states = storage.all("State").values()
    state = [obj.to_dict() for obj in states if obj.id == state_id]
    if state == []:
        abort(404)
    cities = [city.to_dict() for city in storage.all("City").values()
              if state_id == city.state_id]
    return jsonify(cities)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """create a city"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    states = storage.all("State").values()
    state = [obj.to_dict() for obj in states if obj.id == state_id]
    if state == []:
        abort(404)
    cities = []
    new_city = City(name=request.json['name'], state_id=state_id)
    storage.new(new_city)
    storage.save()
    cities.append(new_city.to_dict())
    return jsonify(cities[0]), 201


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """return a city"""
    cities = storage.all("City").values()
    city = [obj.to_dict() for obj in cities if obj.id == city_id]
    if city == []:
        abort(404)
    return jsonify(city[0])


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """delete a specific city"""
    cities = storage.all("City").values()
    city = [obj.to_dict() for obj in cities if obj.id == city_id]
    if city == []:
        abort(404)
    city.remove(city[0])
    for obj in cities:
        if obj.id == city_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """update a city"""
    cities = storage.all("City").values()
    city = [obj.to_dict() for obj in cities if obj.id == city_id]
    if city == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    city[0]['name'] = request.json['name']
    for obj in cities:
        if obj.id == city_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(city[0]), 200
