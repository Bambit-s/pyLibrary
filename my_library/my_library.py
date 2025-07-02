from typing import Dict, List #Python < 3.9
"""ads"""
class Book:
    
    def __init__(self, title:str,author:str,year:int,isbn:str):
        self.title : str = title
        self.author : str = author
        self.year : int = year
        self.isbn : str = isbn
        self.is_borrowed : bool = False
    
    def borrow(self)->None:
        self.is_borrowed=True
            
    def return_book(self)->None:
        self.is_borrowed=False
        
    def __str__(self)->str:
        return f"{self.title}, {self.author}, {self.year}, ISBN: {self.isbn}"
           
class User:
    
    def __init__(self,name:str,user_id:str,borrowed_books:list=None):
        self.name : str = name
        self.user_id : str = user_id
        self.borrowed_books : list = borrowed_books if borrowed_books else []
        
    def borrow_book(self, book:str)->None:
        self.borrowed_books.append(book.__str__())
        return self.borrowed_books
    
    def return_book(self, borrowbook:str):
        borrowbook = borrowbook.__str__()
        if borrowbook in self.borrowed_books:
            self.borrowed_books.remove(borrowbook)
          
    def __str__(self)->str:
        return f"Пользовататель: {self.name} (ID: {self.user_id}) {self.borrowed_books}"
    
class Library():
    
    def __init__(self):
        self.books : dict = {}    
        self.users : dict = {} 
        
    def add_book(self, title:str, author:str, year:int, isbn:str)->str:
        book = Book(title,author,year,isbn)
        if self.check_by_isbn(book):
            return "Такой isbn занят"
        self.books[book.isbn] = book
        return "Книга добавлена"
    
    def check_by_isbn(self, book:object)->bool:
        for isbn in self.books:
            if (isbn) == book.isbn:
                return True     
    
    def add_user(self, name:str, user_id:str)->str:
        new_user= User(name,user_id,[])
        if self.check_by_user(new_user):
            return "User занят! Используйте другой user_id!"
        self.users[new_user.user_id] = new_user
        return "Пользователь добавлен"
    
    def check_by_user(self,new_user:object)->bool:
        for user_id in self.users:
            if user_id==new_user.user_id:
                return True
    
    def borrow_book(self,user_id:str, isbn:str)->str:
        
        if user_id not in self.users:
            return self.UserNotFoundError()
        
        if isbn not in self.books:
            return self.BookNotFoundError()
        
        if not self.check_by_3_books(user_id):
            return "Взято 3 книги!"
        
        if self.books[isbn].is_borrowed:
            return f"Книга {isbn} взята другим пользователем"
        
        user = self.users[user_id]
        book = (self.books)[isbn]
        user.borrow_book(book)
        book.borrow()
    
        return f"{user_id} взял {isbn}"
    
    def check_by_3_books(self,user_id)->bool:
        return len(self.users[user_id].borrowed_books)<3
    
    def return_book(self, user_id:str, isbn:str)->str:
        if isbn in self.books and user_id in self.users:
            borrowBook = self.books[isbn]
            user = self.users[user_id]
            borrowBook.return_book()
            user.return_book(borrowBook)
            return f"Книга {isbn} возвращена"
        return self.BookNotFoundError()
    
    def list_available_books(self)->list:
        return [self.books[book].__str__() for book in self.books
            if (self.books[book].is_borrowed == False)]
        
    def list_borrowed_books(self)->list:
        return [self.books[book].__str__() for book in self.books
            if (self.books[book].is_borrowed == True)]
    
    def search_books(self, title=None, author=None)->list:
        return [book.__str__() for book in self.books.values()
                if (title is None or book.title == title) and
                (author is None or book.author == author)]
        
    def BookNotFoundError(self)->str:
        return "Книга не найдена..."
        
    def UserNotFoundError(self)->str:
        return "User не найден..."
    
lib = Library()
# print(lib.add_book("1984", "George Orwell", 1949, "ISBN-001"))
# print(lib.add_book("1984", "George Orwell", 1949, "ISBN-001"))
# print(lib.add_book("King Arthur", "Merlin", 1927, "ISBN-002"))
# print(lib.add_book("1984", "George", 1945, "ISBN-010"))
# print(lib.add_book("Alladin", "Allah", 1999, "ISBN-003"))
# print(lib.add_book("Prince of Persia", "Unity", 2011, "ISBN-004"))
# print(lib.add_book("1984", "Merlin", 1927, "ISBN-005"))

# print(lib.add_user("Анна", "user-1"))
# print(lib.add_user("Kate", "user-2"))
# print(lib.add_user("Kate", "user-2"))

# print(lib.borrow_book("user-1", "ISBN-001"))
# print(lib.borrow_book("user-1", "ISBN-002"))
# print(lib.users['user-1'])

# # print(lib.borrow_book("user-1", "ISBN-003"))

# lib.list_borrowed_books()
# # # print(lib.search_books("1984"))
# lib.list_available_books()
# print(lib.return_book("user-1", "ISBN-001"))
# print(lib.users['user-1'])
# print(lib.return_book("user-1", "ISBN-002"))
# print(lib.users['user-1'])
# # print(lib.return_book("user-1", "ISBN-001"))
# # print(lib.users)
# # print(lib.borrow_book("user-1", "ISBN-002"))
# # print(lib.users['user-1'])
# # # print(lib.borrow_book("user-1", "ISBN-002"))
# # # print(lib.borrow_book("user-2", "ISBN-005"))
# # # print(lib.borrow_book("user-1", "ISBN-002"))

# # print(lib.search_books("1984"))