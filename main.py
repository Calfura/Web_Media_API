import os
from flask import Flask
from init import db, ma, bcrypt, jwt

def create_app():
    app = Flask(__name__)

    # Unsorting of json key information
    app.json.sort_keys = False

    # Config setting for Flask
    app.config["SQLALCHEMY_DATABASE_URI"]=os.environ.get("DATABASE_URI")
    app.config["JWT_SECRET_KEY"]=os.environ.get("JWT_SECRET_KEY")

    # Calling models from init.py
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Initalizing controller input commands
    from controllers.cli_controller import db_commands
    app.register_blueprint(db_commands)

    from controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    from controllers.profile_controller import profiles_bp
    app.register_blueprint(profiles_bp)

    from controllers.watchlist_controller import watchlists_bp
    app.register_blueprint(watchlists_bp)

    from controllers.content_controller import content_bp
    app.register_blueprint(content_bp)

    return app