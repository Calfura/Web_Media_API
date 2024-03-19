from init import db, ma
from marshmallow import fields

class Content(db.Model):
    __tablename__ = "content"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genre = db.Column(db.String)
    description = db.Column(db.Text)
    duration = db.Column(db.String)

    watchlists = db.relationship('WatchList', back_populates='content')

class ContentSchema(ma.Schema):
    
    watchlists = fields.List(fields.Nested('WatchListSchema'))

    class Meta:
        fields = ('id', 'name', 'genre', 'desciption', 'duration', 'watchlists')

content_schema = ContentSchema()
contetns_schema = ContentSchema(many=True)