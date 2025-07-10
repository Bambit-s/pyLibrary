from flask import Flask
from dbmodels import db

class Database:
    @staticmethod
    def _connection(app):

        app.secret_key = "1234"
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
            
        db.init_app(app)
        
        with app.app_context():
            db.create_all()
            
    