from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from enum import Enum
from flask_login import UserMixin

db = SQLAlchemy()

user_books = db.Table('user_books',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                      db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
                      db.Column('reservation_date', db.DateTime, default=datetime),
                      )

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    
class UserRole(Enum):
    user = 'user'
    librarian = 'librarian'
    admin = 'admin'
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.user, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    reserved_books = db.relationship(
        'Book',
        secondary = user_books,
        backref = db.backref('reserved_by', lazy='dynamic'),
        lazy = 'dynamic'
    )
    
    def get_id(self):
        return str(self.id)
    
    @property
    def is_active(self):
        return True 
    
    def set_password(self,password):
        self.password_hash=generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)