from init import db, ma
from marshmallow import fields

class Profile(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='profiles')
    watchlists = db.relationship('WatchList', back_populates='profiles', cascade='all, delete')

class ProfileSchema(ma.Schema):
    user = fields.Nested('UserSchema', only = ['name', 'email'])
    watchlists = fields.Nested('WatchListSchema')
    
    class Meta:
        fields = ('id', 'name', 'user_id', 'user', 'watchlists')

profile_schema = ProfileSchema()
profiles_schema = ProfileSchema(many=True)