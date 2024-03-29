from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from psycopg2 import errorcodes
from sqlalchemy.exc import IntegrityError
from models.content import Content, contents_schema
from models.watchlist import WatchList, watchlist_schema

content_bp = Blueprint('content', __name__, url_prefix='/<int:profile_id>/<lang_code>/content')

# Fetching all profiles
@content_bp.route('/')
def get_all_content():
    # Selecting all profiles
    stmt = db.select(Content).order_by(Content.name.desc())
    contents = db.session.scalars(stmt)
    # Returns all profiles
    return contents_schema.dump(contents)

@content_bp.route('/<int:content_id>', methods=['POST'])
@jwt_required()
def add_content(profile_id, lang_code, content_id):
    body_data = request.get_json()
    stmt = db.select(Content).filter_by(id=content_id)
    content = db.session.scalar(stmt)
    try:
        if content:
            content = WatchList(
                title = lang_code,
                content_id = body_data.get('content_id'),
                profile_id = get_jwt_identity()
            )

            db.session.add(content)
            db.session.commit()

            return watchlist_schema.dump(content), 201
        else:
            return {"error": f"Content with id {content_id} already exsists in watchlist {lang_code}"}
        
    except IntegrityError as err:
        print(err.orig.pgcode)
        print(err.orig.diag.column_name)
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The watchlist {err.orig.diag.column_name} is required"}
        
@content_bp.route('/<int:content_id>', methods=['DELETE'])
@jwt_required()
def remove_content(profile_id, lang_code, content_id):
    stmt = db.select(WatchList).filter_by(title=lang_code)
    watchlist = db.session.scalar(stmt)
    # Checks for owner of the Watchlist and checks for content to be removed
    if watchlist and watchlist.profiles.id == profile_id and watchlist.content.id == content_id:
        db.session.delete(watchlist)
        db.session.commit()
        # Successfully found. Removes content from list
        return {"message": f"Content with id {content_id} has been removed"}
    # If content_id was not located in owned listed, reports error message
    else:
        return {"error": f"Content with id {content_id} was not found in watchlist {lang_code}"}