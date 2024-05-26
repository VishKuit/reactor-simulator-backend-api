from flask import Blueprint, jsonify, request
from models.reactor import Reactor

web_blueprint = Blueprint("web_blueprint", __name__)


@web_blueprint.route("/")
def hello_geek():
    return "<h2>Hello from Flask & Docker & Blueprints</h2>"


# Endpoint which return the same request data
@web_blueprint.route("/mirror", methods=["POST"])
def mirror():
    data = request.get_json()
    return jsonify(data)


# Create OPTIONS method for /test endpoint to allow CORS
@web_blueprint.route("/test", methods=["OPTIONS"])
def test_options():
    return jsonify({}), 200


# Test endpoint to run the reactor model
@web_blueprint.route("/test", methods=["POST", "OPTIONS"])
def index():
    data = request.get_json()
    reactor = Reactor()
    reactor.setup_reactor(
        RT=data.get("RT", 2),
        FNV=data.get("FNV", 1200),
        VT=data.get("VT", 1),
        P0=data.get("P0", 10),
        T0=data.get("T0", 533.15),
        yA0=data.get("yA0", 0.67),
        yB0=data.get("yB0", 0.33),
        yC0=data.get("yC0", 0),
        yD0=data.get("yD0", 0),
        a=data.get("a", -1),
        b=data.get("b", -0.5),
        c=data.get("c", 1),
        d=data.get("d", 0),
        EA=data.get("EA", 6.40),
        A=data.get("A", 1),
        rA=data.get("rA", 1),
        ti=data.get("ti", 0),
        tf=data.get("tf", 140),
        CEq=data.get("CEq", None),
        pd_eq=data.get("pd_eq", None),
        td_eq=data.get("td_eq", None)
    )
    reactor.run()

    return jsonify(reactor.results)
