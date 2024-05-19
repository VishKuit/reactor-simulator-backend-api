from flask import Blueprint
from flask import jsonify

web_blueprint = Blueprint("web_blueprint", __name__)


@web_blueprint.route("/")
def hello_geek():
    return "<h2>Hello from Flask & Docker & Blueprints</h2>"

@web_blueprint.route("/test")
def index():
    return "This is an example app"