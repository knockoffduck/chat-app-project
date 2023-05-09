from flask import Flask
from flask_cors import CORS

# Define a function to create the Flask application
def create_app():
    # Create a new Flask application instance
    app = Flask(__name__)

    # Set a secret key for the application (used for encryption and other security features)
    app.config["SECRET_KEY"] = "this is a test"

    # Import the views and auth blueprints
    from .views import views
    from .auth import auth

    # Register the views and auth blueprints with the application
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth")

    # Return the Flask application instance
    CORS(app)
    return app
