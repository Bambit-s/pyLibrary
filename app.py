from flask import Flask, render_template, request
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, LoginManager
from flask_login import current_user
from flask import send_from_directory, abort
from forms import *
from flask_migrate import Migrate
from connection import Database
from registration_validate import RegistrationValidate
from dbmodels import db, Book,User,Genres,BookFile,BookImage
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

Database._connection(app)
migrate = Migrate(app,db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'

UPLOAD_IMG_FOLDER = 'static/uploads_imgs'
UPLOAD_BOOK_FOLDER = 'static/uploads_books'

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
    form = BookForm()
    if form.validate_on_submit():
        #need 
        # 1) validation 
        # 2) check for atacks
        book_file = BookFile(
            filename=form.files_book.data.filename,
            filetype=form.files_book.data.filename.split('.')[-1]  # например 'pdf')
        )
        img_file = BookImage(
            filename=form.files_imgs.data.filename,
            filetype=form.files_imgs.data.filename.split('.')[-1]  # например 'pdf')
        )
        new_book = Book(title=form.title.data, author=form.author.data,
                        year=form.year.data, isbn=form.isbn.data,
                        description=form.description.data, genres=Genres[form.genres.data].value,
                        files_imgs=[img_file], files_book=[book_file],
                        )
        
        cover = form.files_imgs.data
        if cover:
            files_imgs = secure_filename(form.files_imgs.data.filename)
            cover_path = os.path.join("static/uploads_imgs", files_imgs)
            form.files_imgs.data.save(cover_path)

        book_file = form.files_book.data
        if book_file:
            book_filename = secure_filename(form.files_book.data.filename)
            book_path = os.path.join("static/uploads_books", book_filename)
            form.files_book.data.save(book_path)
            
        db.session.add(new_book)
        db.session.commit()
    return render_template('add_book.html', title = 'Add new book', form=form)

@app.route('/library')
def show_library():
    books = Book.query.options(db.joinedload(Book.files_imgs)).all()
    return render_template('show_library.html', title = 'Online Library', books = books)

@app.route('/library/<isbn>')
def show_book(isbn):
    selected_book = Book.query.get(isbn)
    if not selected_book:
        return "Книга не найдена", 404
    return render_template('show_book.html', title=selected_book.title, book=selected_book)

@app.route('/download/<int:file_id>')
def download(file_id):
    UPLOAD_FOLDER = os.path.join('static', 'uploads_books')  # Папка с файлами
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    file = BookFile.query.get_or_404(file_id)
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    if not os.path.exists(file_path):
        abort(404)
    
    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        file.filename,
        as_attachment=True,  # Заставляет браузер скачивать файл
        download_name=f"book_{file.book.isbn}_{file.filename}"  # Понятное имя файла
    )

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
    
    form = RegisterForm()

    if form.validate_on_submit():
        #need 
        # 1) validation 
        # 2) check for atacks 
        new_user = User(name=form.name.data,
                        email=form.email.data,
                        password_hash=form.password.data,)
        new_user.set_password(new_user.password_hash)
        db.session.add(new_user)
        db.session.commit()
        return render_template('login.html', form=form)
    return render_template('register.html', title='Registration page', form=form)
    
if __name__ == '__main__':
    
    with app.app_context(): 
        db.create_all()
        
    app.run(debug=True)
    
    