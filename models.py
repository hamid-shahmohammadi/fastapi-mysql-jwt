import datetime as datetime
import sqlalchemy as _sqlalchemy
from sqlalchemy import Column, Date, Integer, String
import sqlalchemy.orm as _orm

import passlib.hash as _hash
import database as _database

class UserModel(_database.Base):
    __tablename__= "users"
    id=_sqlalchemy.Column(_sqlalchemy.Integer,primary_key=True,index=True)
    email=_sqlalchemy.Column(String(64),unique=True,index=True)
    name=_sqlalchemy.Column(String(64))
    phone=_sqlalchemy.Column(String(64))
    password_hash=_sqlalchemy.Column(String(64))
    created_at=_sqlalchemy.Column(_sqlalchemy.DateTime,default=datetime.datetime.utcnow())
    posts = _orm.relationship("Post",back_populates="user")

    def password_verification(self,password:str):
        return _hash.bcrypt.verify(password, self.password_hash)



class UserModel(_database.Base):
    __tablename__="posts"   
    id=_sqlalchemy.Column(_sqlalchemy.Integer,primary_key=True,index=True) 
    user_id=_sqlalchemy.Column(_sqlalchemy.Integer,_sqlalchemy.ForeignKey("users.id"))
    post_title =  _sqlalchemy.Column(String(64),index=True)
    post_description =  _sqlalchemy.Column(String(64),index=True)
    image =  _sqlalchemy.Column(String(64))
    created_at=_sqlalchemy.Column(_sqlalchemy.DateTime,default=datetime.datetime.utcnow())
    user = _orm.relationship("User",back_populates="posts")

