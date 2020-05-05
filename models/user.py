import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True) #Autoincrement
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        
        self.username = username
        self.password = password

    #@classmethod
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()        

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first() # Select * from users where username=username


    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first() # Select * from users where id=_id