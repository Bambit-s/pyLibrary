from flask import Flask, render_template, request
from my_library.my_library import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/add_book', methods = ['GET', 'POST'])
def add_new_book():
    if request.method == 'POST':
        a = Library()
        print(a.add_book(request.form['title'],request.form['author'],request.form['year'],request.form['isbn']))
        print(a.list_available_books())
    return render_template('add_book.html')

@app.route('/library')
def swow_library():
    return render_template('show_library.html', title='Online Library', books=book)

@app.route('/library/<isbn>')
def show_book(isbn):
    selected_book = book.get(isbn)
    if not selected_book:
        return "Книга не найдена", 404
    return render_template('show_book.html', title=selected_book['title'], book=selected_book)

@app.route('/login')
def login():
    return render_template('login.html')
    
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/test_add')
def test_add():
    new_book = Book(title='Test Book', author='Test Author', year=2024, isbn='TEST123')
    db.session.add(new_book)
    db.session.commit()
    
    return 'Книга добавлена'

app.secret_key = "1234"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATTIONS'] = False
db = SQLAlchemy(app)


# class Book(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(150), nullable=False)
#     author = db.Column(db.String(100), nullable=False)
#     year = db.Column(db.Integer)
#     isbn = db.Column(db.String(20), unique=True, nullable=False)
    
if __name__ == '__main__':
    
    # with app.app_context(): 
    #     db.create_all()
        
    app.run(debug=True)
    
    