from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired(), Length(min=6)])
    
class RegisterForm(FlaskForm):
    name = StringField('Name: ', validators=[DataRequired()])
    email = StringField('Email: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired(), Length(min=6)])
    
class BookForm(FlaskForm):
    title = StringField('Title: ', validators=[DataRequired()])
    author = StringField('Author: ', validators=[DataRequired()])
    year = StringField('Year: ', validators=[DataRequired()])
    isbn = StringField('ISBN: ', validators=[DataRequired()])    
    description = TextAreaField('Description: ', validators=[DataRequired()])
    genres = SelectField('Genre: ', choices=[
    ('Default', 'Default'),
    ('Novel', 'Novel'),
    ('Drama', 'Drama'),
    ('Poetry', 'Poetry'),
    ('Fantasy', 'Fantasy'),
    ('Science_Fiction', 'Science Fiction'),
    ('Detective', 'Detective'),
    ('Romance_Novel' , 'Romance Novel'),
    ('Biography' , 'Biography'),
    ('Travel_Literature' , 'Travel Literature'),
    ('Psychology' , 'Psychology'),
    ('Business' , 'Business'),
    ('Cookery' , 'Cookery'),
    ], validators=[Optional()]) 
    
    files_imgs = FileField('Books Photo: ', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Only images!')
    ])
    
    files_book = FileField('Books Files: ', validators=[
        FileAllowed(['pdf', 'epub', 'fb2'], 'Not corret format')
    ])
    
    submit = SubmitField('Save')