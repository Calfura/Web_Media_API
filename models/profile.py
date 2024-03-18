from init import db, ma
from marshmallow import fields

class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

class ProfileSchema(ma.Schema):
    
    class Meta:
        fields = ('id', 'name')

profile_schema = ProfileSchema()
profiles_schema = ProfileSchema(many=True)