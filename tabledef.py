from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

 
engine = create_engine('sqlite:///tutorial.db', echo=True)
Base = declarative_base()
 
# ------------------------ Table for User -----------------------
class User(Base):
    """"""
    __tablename__ = "users"
 
    email = Column(String, primary_key=True)
    username = Column(String)
    password = Column(String)
    birthday = Column(String) 
 
    #----------------------------------------------------------------------
    def __init__(self, username, birthday, email, password):
        """"""
        self.username = username
	self.email = email
        self.password = password
	self.birthday = birthday

    def __repr__(self):
        return "{name='%s', password='%s', email= '%s', birthday = '%s'}" % (
                            self.username, self.password, self.email, self.birthday)
 
# create tables
Base.metadata.create_all(engine)
