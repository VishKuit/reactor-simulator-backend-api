from flask import Blueprint
from flask import jsonify

example_blueprint = Blueprint("example_blueprint", __name__)


@example_blueprint.route("/test")
def index():
    return "This is an example app"


@example_blueprint.route("/data")
def index2():
    puntos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    return jsonify(puntos)
