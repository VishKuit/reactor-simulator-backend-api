from flask import Flask

from routes.web import web_blueprint


app = Flask(__name__)

app.register_blueprint(web_blueprint, url_prefix="/api/v1")


if __name__ == "__main__":
    app.run(debug=True)
