from flask import Flask
from flask_cors import CORS

from routes.web import web_blueprint


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

app.register_blueprint(web_blueprint, url_prefix="/api/v1")


if __name__ == "__main__":
    app.run(debug=True)
