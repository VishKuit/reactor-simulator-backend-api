from flask import Blueprint
from flask import jsonify
from models.reactor import Reactor

web_blueprint = Blueprint("web_blueprint", __name__)


@web_blueprint.route("/")
def hello_geek():
    return "<h2>Hello from Flask & Docker & Blueprints</h2>"

@web_blueprint.route("/test")
def index():
    reactor = Reactor()
    reactor.setup_reactor(
        RT=2,
        FNV=1200,
        VT=1,
        P0=10,
        T0=533.15,
        yA0=0.67,
        yB0=0.33,
        yC0=0,
        yD0=0,
        a=-1,
        b=-0.5,
        c=1,
        d=0,
        EA=6.40,
        A=1,
        rA=1,
        ti=0,
        tf=140,
        CEq=None,
        pd_eq=None,
        td_eq=None
    )
    reactor.run()

    return jsonify(reactor.results)