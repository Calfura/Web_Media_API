from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.watchlist import WatchList, watchlist_schema, watchlists_schema
from models.profile import Profile

watchlists_bp = Blueprint('watchlists', __name__, url_prefix='/watchlist')

# Fetching all watchlists
@watchlists_bp.route('/')
def get_all_watchlist():
    stmt = db.select(WatchList).order_by(WatchList.title.desc())
    watchlists = db.session.scalars(stmt)
    return watchlists_schema.dump(watchlists)

# Fetching single watchlist
@watchlists_bp.route('/<int:watchlists_id>')
def get_one_watchlist(watchlists_id):
    stmt = db.select(WatchList).filter_by(id=watchlists_id)
    watchlist = db.session.scalar(stmt)
    if watchlist:
        return watchlist_schema.dump(watchlist)
    else:
        return {"error": f"Watchlist with id {watchlists_id} does not exsist."}, 404

# Creating a neww watchlist
@watchlists_bp.route('/', methods=['POST'])
@jwt_required()
def create_watchlist():
    body_data = request.get_json()
    watchlist = WatchList(
        title = body_data.get('title'),
        profile_id = Profile(
            user_id = get_jwt_identity
        )
    )
    db.session.add(watchlist)
    db.session.commit

    return watchlist_schema.dump(watchlist), 201
