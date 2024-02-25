#!/usr/bin/python3
"""Scripts that contains place amenitites endpoints"""
from api.v1.views import app_views
from flask import jsonify, abort
from models.place import Place
from models import storage
from models import storage_t
from models.amenity import Amenity


@app_views.route("/places/<place_id>/amenities")
def amenities_place(place_id):
    """get all amenities in a specific place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenities = []

    if storage_t == "db":
        for amenity in place.amenities:
            amenities.append(amenity.to_dict())
    else:
        amenities = place.amenities

    return jsonify(amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"])
def del_amenity_place(place_id, amenity_id):
    """delete amenity in place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place:
        abort(404)
    if not amenity:
        abort(404)
    if amenity not in place.amenities:
        abort(404)

    if storage_t == "db":
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity)
    storage.save()

    return jsonify({})


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"])
def add_amentiy_place(place_id, amenity_id):
    """add amentiy to place."""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place:
        abort(404)
    if not amenity:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict())

    if storage_t == "db":
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity.id)
    storage.save()

    return jsonify(amenity.to_dict()), 201
