from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.profile import Profile, profile_schema, profiles_schema

profiles_bp = Blueprint('profiles', __name__, url_prefix='/profile')

@profiles_bp.route('/')
def get_all_card():
    stmt = db.select(Profile).order_by(Profile.name.desc())
    profiles = db.session.scalars(stmt)
    return profiles_schema.dump(profiles)

@profiles_bp.route('/<int:profiles_id>')
def get_one_profile(profiles_id):
    stmt = db.select(Profile).filter_by(id=profiles_id)
    profile = db.session.scalar(stmt)
    if profile:
        return profile_schema.dump(profile)
    else:
        return {"error": f"Profile with id {profiles_id} does not exsist."}, 404
    
