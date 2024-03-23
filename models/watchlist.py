from init import db, ma
from marshmallow import fields

class WatchList(db.Model):
    __tablename__ = "watchlists"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)

    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'))

    profiles = db.relationship('Profile', back_populates='watchlists')
    content = db.relationship('Content', back_populates='watchlists')

class WatchListSchema(ma.Schema):
    content = fields.Nested('ContentSchema')
    profiles = fields.Nested('ProfileSchema', only=['name'])

    class Meta:
        fields = ('id', 'title', 'content_id', 'profile_id', 'profiles', 'content')
        ordered = True

watchlist_schema = WatchListSchema()
watchlists_schema = WatchListSchema(many=True)