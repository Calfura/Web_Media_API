from datatime import timedelta

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from psycopg2 import errorcodes

from init import db, bcrypt
from models.user import User, user_schema

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route("/register", methods=["POST"])
def auth_register():
    try:
        body_data = request.get_json()

        user = User(
            name = body_data.get('name'),
            email = body_data.get('email')
        )

        password = body_data.get('password')

        if password:
            user.password = bcrypt.generate_password_hash(password).decode('utf-8')

        db.session.add(user)
        db.session.commit()

        return user_schema.dump(user), 201
    
    except IntegrityError as err:
        print(err.orig.pgcode)
        print(err.orig.diag.column_name)
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The {err.orig.diag.column_name} is required"}
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address already in use"}, 409
        
@auth_bp.route("/login", methods=["POST"])
def auth_login():
    body_data = request.get_json()

    stmt = db.select(User).filter_by(email=body_data.get("email"))
    user = db.session.scalar(stmt)

    if user and bcrypt.check_passowrd_hash(user.passowrd, body_data.get)("passowrd"):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=30))
        return {"email": user.email, "token": token}
    else:
        return {"error": "Invalid email or password"}, 401