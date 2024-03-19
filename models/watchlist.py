from init import db, ma
from marshmallow import fields

class WatchList(db.Model):
    __tablename__ = "watchlists"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)

    profiles = db.relationship('Profile', back_populates='watchlists')
    content = db.relationship('Content', back_populates='watchlists')

class WatchListSchema(ma.Schema):
    contents = fields.List(fields.Nested('ContentSchema'))
    profiles = fields.List(fields.Nested('ProfileSchema'))

    class Meta:
        fields = ('id', 'title', 'content_id', 'profile_id', 'profiles', 'contents')

watchlist_schema = WatchListSchema()
watchlists_schema = WatchListSchema(many=True)