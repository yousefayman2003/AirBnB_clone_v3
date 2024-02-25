#!/usr/bin/python3
"""Scripts that contains reviews endpoints"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def reviews(place_id):
    '''get all reviews for a specific place'''
    places = storage.all("Place").values()
    plc = [obj.to_dict() for obj in places if obj.id == place_id]
    if plc == []:
        abort(404)
    reviews = [obj.to_dict() for obj in storage.all("Review").values()
               if place_id == obj.place_id]
    return jsonify(reviews)


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def crt_review(place_id):
    '''create review'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    user_id = request.json['user_id']
    if 'text' not in request.get_json():
        abort(400, 'Missing text')
    places = storage.all("Place").values()
    plc = [obj.to_dict() for obj in places if obj.id == place_id]
    if plc == []:
        abort(404)
    all_users = storage.all("User").values()
    user_obj = [obj.to_dict() for obj in all_users if obj.id == user_id]
    if user_obj == []:
        abort(404)
    reviews = []
    new_review = Review(text=request.json['text'], place_id=place_id,
                        user_id=user_id)
    storage.new(new_review)
    storage.save()
    reviews.append(new_review.to_dict())
    return jsonify(reviews[0]), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET'])
def review(review_id):
    '''get review'''
    reviews = storage.all("Review").values()
    review = [obj.to_dict() for obj in reviews if obj.id == review_id]
    if review == []:
        abort(404)
    return jsonify(review[0])


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_review(review_id):
    '''delete review'''
    reviews = storage.all("Review").values()
    review = [obj.to_dict() for obj in reviews if obj.id == review_id]
    if review == []:
        abort(404)
    review.remove(review[0])
    for obj in reviews:
        if obj.id == review_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['PUT'])
def updt_review(review_id):
    '''update review'''
    reviews = storage.all("Review").values()
    review = [obj.to_dict() for obj in reviews if obj.id == review_id]
    if review == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'text' in request.get_json():
        review[0]['text'] = request.json['text']
        for obj in reviews:
            if obj.id == review_id:
                obj.text = request.json['text']
        storage.save()
    return jsonify(review[0]), 200
