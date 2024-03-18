from init import db, ma
from marshmallow import fields

class WatchList(db.Model):
    __tablename__ = "watchlists"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content_id = db.Column(db.String)
    profile_id = db.Column(db.String)

class WatchListSchema(ma.Schema):
    
    fields = ('id', 'title', 'content_id', 'profile_id')

watchlist_schema = WatchListSchema()
watchlists_schema = WatchListSchema(many=True)