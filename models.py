from datetime import datetime
from config import db, ma
from marshmallow_sqlalchemy import ModelSchema

class Person(db.Model):
    __tablename__ = "person"
    person_id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32))
    fname = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class PersonSchema(ModelSchema):
    class Meta:
        model = Person
        sqla_session = db.session

class Book(db.Model):
    __tablename__="Book"
    isbn= db.Column(db.Integer,
                    primary_key=True)
    title = db.Column(db.String(64))
    course = db.Column(db.String(64))
    editorial = db.Column(db.String(64))
    subject = db.Column(db.String(64))
    total_quantity = db.Column(db.Integer)
    avaliable_quantity = db.Column(db.Integer)
    entry_date = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)

class BookSchema(ma.ModelSchema):
    class Meta:
        model = Book
        sqla_session = db.session     

class Sample(db.Model):
        __tablename__="Sample"
        id = db.Column(db.String(15),
                       primary_key=True)
        status = db.Column(db.String(64))
        isbn = db.Column(db.Integer,
                         ForeignKey("Book.isbn"))
        donator = db.Column(db.String(64),
                            ForeignKey("User.id"))
        reciever = db.Column(db.String(64),
                             ForeignKey("User.id"),nullable=True)
        latitude = db.Column(db.String(64))
        longitude = db.Column(db.String(64))
        city = db.Column(db.String(64))

class SampleSchema(ma.ModelSchema):
    class Meta:
        model = Sample
        sqla_session = db.session
      
class User(db.Model):
    __tablename__="User"
    id = db.Column(db.String(15),
                       primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))
    email = db.Column(db.String(64))
    logic_deleted = db.Column(db.Boolean,Default=False)

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        sqla_session = db.session
     
class Photo(db.Model):
    __tablename__="Photo"
    id = db.Column(db.String(15),
                       primary_key=True)
    sample_id = db.Column(db.String(64),
                            ForeignKey("Sample.id"))

class PhotoSchema(ma.ModelSchema):
    class Meta:
        model = Photo
        sqla_session = db.session
 
class Message(db.Model):
    __tablename__="Message"
    id = db.Column(db.String(15),
                       primary_key=True)
    content = db.Column(db.String(512))
    donator = db.Column(db.String(64),
                            ForeignKey("User.id"))
    reciever = db.Column(db.String(64),
                             ForeignKey("User.id"))
    send_date = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)

class MessageSchema(ma.ModelSchema):
    class Meta:
        model = Message
        sqla_session = db.session
        
    