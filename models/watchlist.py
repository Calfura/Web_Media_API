from init import db, ma
from marshmallow import fields

class WatchList(db.Model):
    __tablename__ = "watchlists"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    content_id = db.Column(db.Integer, db.ForeignKey("content.id"), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"), nullable=False)

    profile = db.relationship('Profile', back_populates='watchlists')

class WatchListSchema(ma.Schema):
    content = fields.List(fields.Nested('ContentSchema', exclude=['user']))
    profile = fields.List(fields.Nested('ProfileSchema', exclude=['user']))

    class Meta:
        fields = ('id', 'title', 'content_id', 'profile_id')

watchlist_schema = WatchListSchema()
watchlists_schema = WatchListSchema(many=True)