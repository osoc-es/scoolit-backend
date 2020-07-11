from flask_sqlalchemy import SQLAlchemy

class User(db.Model):
    id = db.column('student_id', db.Integer, primary_key=True) 
    usesrname = db.column(db.String(100))
    password = db.column(db.String(100))
    email = db.column(db.String(100))
    deleted = db.column(db.Boolean)
