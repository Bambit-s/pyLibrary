from flask_wtf import FlaskForm
from wtforms import *
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, EqualTo,ValidationError
from dbmodels import User

def email_login(form,field):
    if not User.query.filter_by(email=field.data).first():
        raise ValidationError('Email not found ') 
    
class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=
                        [DataRequired(),
                        email_login
                        ])
    password = PasswordField('Password: ', validators=[DataRequired(), Length(min=6)])

def email_exists(form,field):
    if User.query.filter_by(email=field.data).first():
        raise ValidationError('Email is closed')    
    
class RegisterForm(FlaskForm):
    name = StringField('Name: ', validators=[DataRequired()])
    email = StringField('Email: ', validators=[
        DataRequired(message="Important field"),
        Email(message='Not correct email!'),
        email_exists
        ])
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