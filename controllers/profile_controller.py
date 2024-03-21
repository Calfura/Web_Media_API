from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.profile import Profile, profile_schema, profiles_schema


profiles_bp = Blueprint('profiles', __name__, url_prefix='/profile')

# Fetching all profiles
@profiles_bp.route('/')
def get_all_profile():
    # Selecting all profiles
    stmt = db.select(Profile).order_by(Profile.name.desc())
    profiles = db.session.scalars(stmt)
    # Returns all profiles
    return profiles_schema.dump(profiles)

# Fetching single profile
@profiles_bp.route('/<int:profiles_id>')
def get_one_profile(profiles_id):
    # Selecting profile_id from Profile class
    stmt = db.select(Profile).filter_by(id=profiles_id)
    profile = db.session.scalar(stmt)
    if profile:
        # Returns profile
        return profile_schema.dump(profile)
    else:
        # Return error of id not found
        return {"error": f"Profile with id {profiles_id} does not exsist."}, 404

# Creating new profile
@profiles_bp.route("/", methods=['POST'])
# Requires login
@jwt_required()
def profile_create():
    body_data = request.get_json()
    # Creating profile
    profile = Profile(
        name = body_data.get('name'),
        user_id = get_jwt_identity()
    )
    # Add and commiting profile to database
    db.session.add(profile)
    db.session.commit
    # Return newly made profile and code
    return profile_schema.dump(profile),201