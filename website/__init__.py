from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'

# Define a function to create the Flask application
def create_app(config_class=Config):
    # Create a new Flask application instance
    app = Flask(__name__)

    # Set a secret key for the application (used for encryption and other security features)
    app.config["SECRET_KEY"] = "this is a test"

    # Database setup
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    app.app_context().push()

    from website import views, auth, models

    # Import the views and auth blueprints
    from .views import views
    from .auth import auth

    # Register the views and auth blueprints with the application
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth")


    # Import load_user to avoid circular import error
    from .models import load_user, User

    # Register the user loader function with Flask-Login
    login.user_loader(load_user)

    # Return the Flask application instance
    return app