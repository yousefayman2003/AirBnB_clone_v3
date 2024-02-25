#!/usr/bin/python3
"""Script that handles amenities endpoints"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET'])
def amenities():
    '''gets all amenities'''
    amenities = [obj.to_dict() for obj in storage.all("Amenity").values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def amenity(amenity_id):
    '''get an amenitity'''
    amenities = storage.all("Amenity").values()
    amenity = [obj.to_dict() for obj in amenities
               if obj.id == amenity_id]
    if amenity == []:
        abort(404)
    return jsonify(amenity[0])


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def del_amenity(amenity_id):
    '''delete an amenitiy'''
    amenities = storage.all("Amenity").values()
    amenity = [obj.to_dict() for obj in amenities
               if obj.id == amenity_id]
    if amenity == []:
        abort(404)
    amenity.remove(amenity[0])
    for obj in amenities:
        if obj.id == amenity:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'])
def crt_amenity():
    '''create an amenity'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    amenities = []
    amenity = Amenity(name=request.json['name'])
    storage.new(amenity)
    storage.save()
    amenities.append(amenity.to_dict())
    return jsonify(amenities[0]), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def updt_amenity(amenity_id):
    '''update an amenity'''
    amenities = storage.all("Amenity").values()
    amenity = [obj.to_dict() for obj in amenities
               if obj.id == amenity_id]
    if amenity == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    amenity[0]['name'] = request.json['name']
    for obj in amenities:
        if obj.id == amenity_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(amenity[0]), 200
