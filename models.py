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
    isbn = db.Column(db.String(64), primary_key=True)
    title = db.Column(db.String(64))
    course = db.Column(db.String(64))
    editorial = db.Column(db.String(64))
    subject = db.Column(db.String(64))
    total_quantity = db.Column(db.Integer)
    avaliable_quantity = db.Column(db.Integer)
    entry_date = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)

class BookSchema(ModelSchema):
    class Meta:
        model = Book
        sqla_session = db.session     

class Sample(db.Model):
        __tablename__="Sample"
        id = db.Column(db.Integer, primary_key=True)
        status = db.Column(db.String(64))
        isbn = db.Column(db.String(64),
                         db.ForeignKey("Book.isbn"))
        donator = db.Column(db.Integer,db.ForeignKey("User.id"))
        receiver = db.Column(db.Integer,db.ForeignKey("User.id"),nullable=True)
        latitude = db.Column(db.String(64))
        longitude = db.Column(db.String(64))
        city = db.Column(db.String(64))

class SampleSchema(ModelSchema):
    class Meta:
        model = Sample
        sqla_session = db.session
      
class User(db.Model):
    __tablename__="User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))
    email = db.Column(db.String(64))
    logic_deleted = db.Column(db.Boolean,default=False)

class UserSchema(ModelSchema):
    class Meta:
        model = User
        sqla_session = db.session
     
class Photo(db.Model):
    __tablename__="Photo"
    id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.Integer,
                            db.ForeignKey("Sample.id"))

class PhotoSchema(ModelSchema):
    class Meta:
        model = Photo
        sqla_session = db.session
 
class Message(db.Model):
    __tablename__="Message"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(512))
    donator = db.Column(db.Integer,
                            db.ForeignKey("User.id"))
    receiver = db.Column(db.Integer,
                             db.ForeignKey("User.id"))
    send_date = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)

class MessageSchema(ModelSchema):
    class Meta:
        model = Message
        sqla_session = db.session
