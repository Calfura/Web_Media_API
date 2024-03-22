from init import db, ma
from marshmallow import fields

class Profile(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    
    # User_id for each owned profile
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # User to profile relation
    user = db.relationship('User', back_populates='profiles')
    
    # Profile to Watchlists relation
    watchlists = db.relationship('WatchList', back_populates='profiles', cascade='all, delete')

class ProfileSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name', 'email'])
    watchlists = fields.Nested('WatchListSchema', only=['title'])
    
    class Meta:
        fields = ('id', 'name', 'user', 'profiles')

profile_schema = ProfileSchema()
profiles_schema = ProfileSchema(many=True)