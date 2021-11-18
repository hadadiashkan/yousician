import importlib
import json
import os

from flask import Flask, request
from marshmallow import ValidationError

from application.extensions import mongo
from utils.response import custom_jsonify


def create_app(config_filename):
    # __name__ : current Python module
    app = Flask("application", static_folder="utabib-flask-backend")
    app.config.from_object(config_filename)

    @app.route("/<path:path>")
    def serve_static_files(path):
        return app.send_static_file(path)

    mongo.init_app(app)

    for installed_app_resources in app.config["INSTALLED_RESOURCES"]:
        app_resource = importlib.import_module(f"views.{installed_app_resources}")
        app.register_blueprint(app_resource.get_resources())

    # CREATE STATIC FOLDER:
    static_folder_path = app.config["UPLOAD_DIR"]
    if not os.path.exists(static_folder_path):
        os.makedirs(static_folder_path)
        os.makedirs(static_folder_path + "/user")
        os.makedirs(static_folder_path + "/category")

    @app.errorhandler(404)
    def resource_not_found(e):
        return (
            json.dumps({"message": "Page Not Found!"}),
            404,
            {"Content-Type": "application/json"},
        )

    @app.errorhandler(ValidationError)
    def handle_marshmallow_errors(error):
        return custom_jsonify(
            error_msg=error.messages, status_code=400, error_type="ValidationError"
        )

    @app.before_request
    def handle_option_request():
        if request.method == "OPTIONS":
            return custom_jsonify(status_code=200, data={})

    return app
