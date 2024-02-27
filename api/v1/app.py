#!/usr/bin/python3
"""
Instance of Flask app
"""
import os
from flask import Flask
from models import storage
from werkzeug.exceptions import NotFound
from api.v1.views import app_views
from flask import jsonify

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(NotFound)
def handle_404(error):
    """Handle 404 errors"""
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Closes the storage"""
    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
