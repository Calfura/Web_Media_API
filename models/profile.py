from init import db, ma
from marshmallow import fields

class Profile(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='profiles')

class ProfileSchema(ma.Schema):
    user = fields.Nested('UserSchema', only = ['name', 'email'])
    
    class Meta:
        fields = ('id', 'name', 'user')

profile_schema = ProfileSchema()
profiles_schema = ProfileSchema(many=True)