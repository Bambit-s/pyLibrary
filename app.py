from flask import Flask, render_template, request
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, LoginManager
from flask_login import current_user
from login_form import LoginForm
from flask_migrate import Migrate
from connection import Database
from dbmodels import db, Book,User


app = Flask(__name__)

Database._connection(app)
migrate = Migrate(app,db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/add_book', methods = ['POST','GET'])
@login_required
def add_new_book():
    if request.method == 'POST':
        #need 
        # 1) validation 
        # 2) check for atacks 
        new_book = Book(title=request.form['title'],author=request.form['author'],year=request.form['year'],isbn=request.form['isbn'])
        db.session.add(new_book)
        db.session.commit()
    return render_template('add_book.html', title = 'Add new book')

@app.route('/library')
def show_library():
    return render_template('show_library.html', title = 'Online Library', books = Book.query.all())

@app.route('/library/<isbn>')
def show_book(isbn):
    selected_book = Book.query.get(isbn)
    if not selected_book:
        return "Книга не найдена", 404
    return render_template('show_book.html', title=selected_book.title, book=selected_book)

@app.route('/login', methods = ['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            flash('Вы успешно вошли в систему!', 'success')
            login_user(user)
            return redirect(url_for('profile'))
        flash('Неверный логин или пароль', 'danger')
    return render_template('login.html', form=form)

@app.route('/profile')
@login_required
def profile():
    flash('Вы вошли в систему', 'info')
    return render_template('profile.html', user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('login'))

@app.route('/register', methods = ['POST','GET'])
def register():
    if request.method == 'POST':
        #need 
        # 1) validation 
        # 2) check for atacks 
        new_user = User(name=request.form['name'],role='user',email=request.form['email'],password_hash=request.form['password'])
        new_user.set_password(new_user.password_hash)
        db.session.add(new_user)
        db.session.commit()
    return render_template('register.html', title='Registration page')
    
if __name__ == '__main__':
    
    with app.app_context(): 
        db.create_all()
        
    app.run(debug=True)
    
    