#!/usr/bin/python3
"""
RESTful API actions for Cities
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):
	"""Get all cities for a given state"""
	state = storage.get(State, state_id)
	if state is None:
		abort(404)
	city_list = []
	for city in state.cities:
		city_list.append(city.to_dict())
	return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
	"""Gets a single city"""
	city = storage.get(City, city_id)
	if city is None:
		abort(404)
	return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
	"""Deletes a city"""
	city = storage.get(City, city_id)
	if city is None:
		abort(404)
	storage.delete(city)
	storage.save()
	return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
	"""Creates a city"""
	state = storage.get(State, state_id)
	if state is None:
		abort(404)
	if not request.json:
		abort(400, "Not a JSON")
	if 'name' not in request.json:
		abort(400, "Missing name")
	data = request.get_json()
	city = City(**data)
	city.state_id = state_id
	storage.new(city)
	storage.save()
	return jsonify(city.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
	"""Updates a city"""
	city = storage.get(City, city_id)
	if city is None:
		abort(404)
	if not request.json:
		abort(400, "Not a JSON")
	data = request.get_json()
	for key, value in data.items():
		if key not in ['id', 'state_id', 'created_at', 'updated_at']:
			setattr(city, key, value)
	storage.save()
	return jsonify(city.to_dict()), 200
