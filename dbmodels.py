from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from enum import Enum 
from flask_login import UserMixin

db = SQLAlchemy()

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'epub', 'fb2'}

user_books = db.Table('user_books',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                      db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
                      db.Column('reservation_date', db.DateTime, default=datetime),
                      )

class Genres(Enum):
    Default = "Default"
    Novel = 'Novel'
    Drama = 'Drama'
    Poetry = 'Poetry'
    Fantasy = 'Fantasy'
    Science_Fiction = 'Science Fiction'
    Detective = 'Detective'
    Romance_Novel = 'Romance Novel'
    Biography = 'Biography'
    Travel_Literature = 'Travel Literature'
    Psychology = 'Psychology'
    Business = 'Business'
    Cookery = 'Cookery'

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(250),nullable=False)
    genres = db.Column(db.Enum(Genres), default=Genres.Default, nullable=False)
    files_imgs = db.relationship('BookImage', backref='book', lazy=True) # one to any
    files_book = db.relationship('BookFile', backref='book', lazy=True) # one to any
    createdata = db.Column(db.DateTime, server_default=func.now())
    updatedate = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    
class BookFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False) 
    filename = db.Column(db.String(100), nullable=False)
    filetype = db.Column(db.String(20), nullable=False)  # pdf, epub ..
    createdata = db.Column(db.DateTime, server_default=func.now())
    updatedate = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

class BookImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    filetype = db.Column(db.String(20), nullable=False)  # img ..
    createdata = db.Column(db.DateTime, server_default=func.now())
    updatedate = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    
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
    createdata = db.Column(db.DateTime, server_default=func.now())
    updatedate = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    
    def get_id(self):
        return str(self.id)
    
    @property
    def is_active(self):
        return True 
    
    def set_password(self,password):
        self.password_hash=generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)