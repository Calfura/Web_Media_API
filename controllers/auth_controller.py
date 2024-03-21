from datetime import timedelta

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from psycopg2 import errorcodes

from init import db, bcrypt
from models.user import User, user_schema

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Creating new user
@auth_bp.route("/register", methods=["POST"])
def auth_register():
    try:
        body_data = request.get_json()

        # Fetching data from JSON to create new user
        user = User(
            name = body_data.get('name'),
            email = body_data.get('email')
        )

        password = body_data.get('password')

        # If has password, generates hex password
        if password:
            user.password = bcrypt.generate_password_hash(password).decode('utf-8')

        db.session.add(user)
        db.session.commit()

        return user_schema.dump(user), 201
    
    # Incorrect input or email already in use
    except IntegrityError as err:
        print(err.orig.pgcode)
        print(err.orig.diag.column_name)
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # Invaild password or empty field
            return {"error": f"The {err.orig.diag.column_name} is required"}
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            # Error message for email already in use
            return {"error": "Email address already in use"}, 409

# Login user
@auth_bp.route("/login", methods=["POST"])
def auth_login():
    body_data = request.get_json()

    stmt = db.select(User).filter_by(email=body_data.get("email"))
    user = db.session.scalar(stmt)
    # Checks if user and password is correct
    if user and bcrypt.check_password_hash(user.password, body_data.get("password")):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=30))
        # Correct user and password. Logged in
        return {"email": user.email, "token": token}
    else:
        # Incorrect user or password. Sends error message
        return {"error": "Invalid email or password"}, 401