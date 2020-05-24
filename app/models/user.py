from app.extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)


    def __init__(self, username):
        self.username = username
 

    @staticmethod
    def find_or_create_from_token(userinfo_response):

        """Find existing user or create new User instance"""
        instance = User.query.filter_by(username=userinfo_response.json()["given_name"]).first()

        if not instance:
            instance = User(userinfo_response.json()["given_name"])
            db.session.add(instance)
            db.session.commit()

        return instance

    @staticmethod
    def get_id(user_id):
        return None
    def __repr__(self):
        return "<User: {}>".format(self.username)
