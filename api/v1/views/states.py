#!/usr/bin/python3
"""
RESTful API actions for States
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
	"""Gets a list of all states"""
	state_list = []
	for state in storage.all(State).values():
		state_list.append(state.to_dict())
	return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
	"""Gets a single state"""
	state = storage.get(State, state_id)
	if state is None:
		abort(404)
	return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
	"""Deletes a state"""
	state = storage.get(State, state_id)
	if state is None:
		abort(404)
	storage.delete(state)
	storage.save()
	return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
	"""Creates a state"""
	if not request.json:
		abort(400, "Not a JSON")
	if 'name' not in request.json:
		abort(400, "Missing name")
	data = request.get_json()
	state = State(**data)
	storage.new(state)
	storage.save()
	return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
	"""Updates a State object"""
	state = storage.get(State, state_id)
	if state is None:
		abort(404)
	if not request.json:
		abort(400, "Not a JSON")
	data = request.get_json()
	for key, value in data.items():
		if key not in ['id', 'created_at', 'updated_at']:
			setattr(state, key, value)
	storage.save()
	return jsonify(state.to_dict()), 200
