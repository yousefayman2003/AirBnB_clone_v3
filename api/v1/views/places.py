#!/usr/bin/python3
"""Scripts that contains users endpoints"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def places_city(city_id):
    '''get all places in a specific city'''
    cities = storage.all("City").values()
    city = [obj.to_dict() for obj in cities if obj.id == city_id]
    if city == []:
        abort(404)
    places = [obj.to_dict() for obj in storage.all("Place").values()
              if city_id == obj.city_id]
    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET'])
def place(place_id):
    '''get place'''
    places = storage.all("Place").values()
    place = [obj.to_dict() for obj in places if obj.id == place_id]
    if place == []:
        abort(404)
    return jsonify(place[0])


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_place(place_id):
    '''delete place'''
    places = storage.all("Place").values()
    place = [obj.to_dict() for obj in places
             if obj.id == place_id]
    if place == []:
        abort(404)
    place.remove(place[0])
    for obj in places:
        if obj.id == place_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def crt_place(city_id):
    '''create place'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    all_cities = storage.all("City").values()
    city = [obj.to_dict() for obj in all_cities
            if obj.id == city_id]
    if city == []:
        abort(404)
    places = []
    new_place = Place(name=request.json['name'],
                      user_id=request.json['user_id'], city_id=city_id)
    all_users = storage.all("User").values()
    user_obj = [obj.to_dict() for obj in all_users
                if obj.id == new_place.user_id]
    if user_obj == []:
        abort(404)
    storage.new(new_place)
    storage.save()
    places.append(new_place.to_dict())
    return jsonify(places[0]), 201


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['PUT'])
def updt_place(place_id):
    '''update place'''
    places = storage.all("Place").values()
    place = [obj.to_dict() for obj in places if obj.id == place_id]
    if place == []:
        abort(404)

    if not request.get_json():
        abort(400, 'Not a JSON')

    fields = ['name', 'description', 'number_rooms', 'number_bathrooms',
              'max_guest', 'price_by_night', 'latitude', 'longitude']
    for field in fields:
        if field in request.get_json():
            place[0][field] = request.json[field]

    for obj in places:
        if obj.id == place_id:
            for field in fields:
                if field in request.get_json():
                    obj.field = request.json[field]
    storage.save()
    return jsonify(place[0]), 200
