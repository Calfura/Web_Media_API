from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.watchlist import WatchList, watchlist_schema
from models.profile import Profile

watchlists_bp = Blueprint('watchlists', __name__, url_prefix='/<int:profile_id>/watchlist')

# Creating a new watchlist
@watchlists_bp.route('/', methods=['POST'])
@jwt_required()
def create_watchlist(profile_id):
    body_data = request.get_json()
    stmt = db.select(Profile).filter_by(id=profile_id)
    profile = db.session.scalar(stmt)

    if profile:
        watchlist = WatchList(
            title = body_data.get('title'),
            profile_id = get_jwt_identity()
        )

        db.session.add(watchlist)
        db.session.commit()

        return watchlist_schema.dump(watchlist), 201
    else:
        return {"error": f"Profile with id {profile_id} does not exsist"}, 404
    
@watchlists_bp.route('/<lang_code>', methods=['DELETE'])
@jwt_required()
def delete_watchlist(profile_id, lang_code):
    stmt = db.select(WatchList).filter_by(title=lang_code)
    watchlist = db.session.scalar(stmt)
    while watchlist and watchlist.profiles.id == profile_id:
        # Queries for all related watchlists and deletes them
        # Checks for owner
        db.session.query(WatchList).filter(WatchList.title==lang_code, WatchList.profile_id==profile_id).delete()
        db.session.commit()
        return {"message": f"Watchlist with id {lang_code} has been deleted"}, 201
    else:
        return {"error": f"Watchlist with id {lang_code} was not found in profile with id {profile_id}"}, 404
    
@watchlists_bp.route('/<int:watchlist_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def add_watchlist(profile_id, watchlist_id, content_id):
    body_data = request.get_json()
    stmt = db.select(WatchList).filter_by(id=watchlist_id, profile_id=profile_id)
    watchlist = db.session.scalar(stmt)
    if watchlist:
        watchlist.content.id = body_data.get('content_id') or watchlist.content.id
        db.session.commit()
        return watchlist_schema.dump(watchlist)
    else:
        return {"error": f"Content with id {content_id} already exsists inside watchlist {watchlist_id}"}