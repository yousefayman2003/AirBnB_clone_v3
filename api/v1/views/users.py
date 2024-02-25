#!/usr/bin/python3
"""Scripts that contains users endpoints"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users/', strict_slashes=False, methods=['GET'])
def users():
    '''get users'''
    users = [obj.to_dict() for obj in storage.all("User").values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def user(user_id):
    '''get a user'''
    users = storage.all("User").values()
    user = [obj.to_dict() for obj in users if obj.id == user_id]

    if user == []:
        abort(404)
    return jsonify(user[0])


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def del_user(user_id):
    '''delete a user'''
    users = storage.all("User").values()
    user = [obj.to_dict() for obj in users if obj.id == user_id]

    if user == []:
        abort(404)
    user.remove(user[0])

    for obj in users:
        if obj.id == user_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/users/', strict_slashes=False, methods=['POST'])
def crt_user():
    '''create user'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'email' not in request.get_json():
        abort(400, 'Missing name')
    if 'password' not in request.get_json():
        abort(400, 'Missing name')

    users = []
    new_user = User(email=request.json['email'],
                    password=request.json['password'])

    storage.new(new_user)
    storage.save()
    users.append(new_user.to_dict())
    return jsonify(users[0]), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def updt_user(user_id):
    '''update a user'''
    users = storage.all("User").values()
    user = [obj.to_dict() for obj in users if obj.id == user_id]

    if user == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')

    try:
        user[0]['first_name'] = request.json['first_name']
    except Exception:
        pass
    try:
        user[0]['last_name'] = request.json['last_name']
    except Exception:
        pass

    for obj in users:
        if obj.id == user_id:
            try:
                if request.json['first_name'] is not None:
                    obj.first_name = request.json['first_name']
            except Exception:
                pass

            try:
                if request.json['last_name'] is not None:
                    obj.last_name = request.json['last_name']
            except Exception:
                pass

    storage.save()
    return jsonify(user[0]), 200
