from init import db, ma
from marshmallow import fields

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    profiles = db.relationship('Profile', back_populates='user', cascade='all, delete')

class UserSchema(ma.Schema):
    profiles = fields.List(fields.Nested('ProfileSchema', exclude=['user']))

    class Meta:
        fields = ('id', 'name', 'email', 'password', 'profiles')

user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(many=True, exclude=['password'])
