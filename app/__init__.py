from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from app.config import Config
from flask_cors import CORS

def create_app():
    # Initialize the Flask application
    app = Flask(__name__)
    CORS(app) 
    # Load configuration from the Config class
    app.config.from_object(Config)

    # Register Blueprints
    from app.routes import routes
    app.register_blueprint(routes)

    # Swagger UI setup
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.yaml'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Song Similarity Analyzer API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Additional initialization (e.g., logging setup, database connections)
    # from app import db  # Uncomment if using a database
    # db.init_app(app)  # Uncomment if using a database

    return app
