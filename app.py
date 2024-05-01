from flask import Flask

from example_blueprint import example_blueprint


app = Flask(__name__)


# @app.route("/")
# def hello_geek():
#     return "<h2>Hello from Flask & Docker</h2>"


# if __name__ == "__main__":
#     app.run(debug=True)


app.register_blueprint(example_blueprint, url_prefix="/example")


if __name__ == "__main__":
    app.run(debug=True)
