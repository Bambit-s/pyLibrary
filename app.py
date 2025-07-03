from flask import jsonify
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from my_library.my_library import *

app = Flask(__name__)

class Lib:
    def __init__(self):
        self.lib = Library()
        self.lib.add_book("1984", "George Orwell", 1949, "ISBN-001")
    def show(self):
      return self.lib.list_available_books()

# Создаем экземпляр класса один раз
my_lib = Lib().show()
# print(my_lib)

@app.route('/hello', methods=['GET'])
def hello():
    # Передаем экземпляр класса в шаблон
    return render_template('hello.html', my_lib=my_lib)

if __name__ == '__main__':
    app.run(debug=True)