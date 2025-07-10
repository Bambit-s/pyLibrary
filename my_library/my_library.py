from typing import Dict, List #Python < 3.9
from abc import ABC, abstractmethod


class Abstract_Book(ABC):

    @abstractmethod
    def _borrow_book(self)->None:
        pass
    
    @abstractmethod
    def _return_book(self)->None:
        pass    
    
class Abstract_User(ABC):
    
    @abstractmethod
    def _borrow_book(self,book: Abstract_Book)->None:
        pass
    
    @abstractmethod
    def _return_book(self,borrowbook: Abstract_Book)->None:
        pass    

class Abstract_Library(ABC):
    
    @abstractmethod
    def add_book(self, title:str, author:str, year:int, isbn:int)->str:
        pass    

    @abstractmethod
    def add_user(self, name:str, user_id:int)->str:
        pass
    
    @abstractmethod
    def borrow_book(self, user_id:int, isbn:int)->str:
        pass
    
    @abstractmethod
    def return_book(self, user_id:int, isbn:int)->str:
        pass
    
    @abstractmethod
    def search_books(self, title=None, author=None)->list[str]:
        pass

class ErrorMixin:
    
    def BookNotFoundError(self) -> str:
        return "Книга не найдена"
    
    def UserNotFoundError(self) -> str:
        return "Пользователь не найден"

class Book(Abstract_Book):

    def __init__(self, title:str,author:str,year:int,isbn:int)->dict:

        self.title : str = title
        self.author : str = author
        self.year : int = year
        self.isbn : int = isbn
        self.is_borrowed : bool = False
    
    def _borrow_book(self)->None:
        self.is_borrowed=True
            
    def _return_book(self)->None:
        self.is_borrowed=False
        
    def __dict__(self)->dict:
        return {"title":self.title, 
                "author":self.author, 
                "year":self.year, 
                "isbn":self.isbn}
           
class User(Abstract_User):
    
    def __init__(self,name:str,user_id:int,borrowed_books:dict=None):
        self.name : str = name
        self.user_id : int = user_id
        self.borrowed_books : dict = borrowed_books if borrowed_books else []
        
    def _borrow_book(self, book:str)->List:
        self.borrowed_books.append(book.__dict__())
        return self.borrowed_books
    
    def _return_book(self, borrowbook:str)->None:
        borrowbook = borrowbook.__dict__()
        if borrowbook in self.borrowed_books:
            self.borrowed_books.remove(borrowbook)
          
    def __dict__(self)->dict:
        return {"name":self.name, 
                "user_id":self.user_id, 
                "borrowed_books":self.borrowed_books}
    
class Library(Abstract_Library, User, Book, ErrorMixin):
    
    def __init__(self):
        self.books : dict = {}    
        self.users : dict = {} 
        self.borrow_books : dict = {}
        
    def add_book(self, title:str, author:str, year:int, isbn:int)->str:
        book = Book(title,author,year,isbn)
        if self.__check_by_isbn(book):
            return "Такой isbn занят"
        self.books[book.isbn] = book
        return "Книга добавлена"
    
    def __check_by_isbn(self, book:object)->bool:
        for isbn in self.books:
            if (isbn) == book.isbn:
                return True     
    
    def add_user(self, name:str, user_id:int)->str:
        new_user= User(name,user_id,{})
        if self.__check_by_user(new_user):
            return "User занят! Используйте другой user_id!"
        self.users[new_user.user_id] = new_user
        return "Пользователь добавлен"
    
    def __check_by_user(self, new_user:object)->bool:
        for user_id in self.users:
            if user_id==new_user.user_id:
                return True
    
    def borrow_book(self, user_id:int, isbn:int)->str:
        
        if user_id not in self.users:
            return self.UserNotFoundError()
        
        if isbn not in self.books:
            return self.BookNotFoundError()
        
        if not self.__check_by_3_books(user_id):
            return "Взято 3 книги!"
        
        if self.books[isbn].is_borrowed:
            return f"Книга {isbn} взята другим пользователем"
        
        user = self.users[user_id]
        book = (self.books)[isbn]
        
        self.borrow_books[isbn]=book
        
        user._borrow_book(book)
        book._borrow_book()
        
        return f"User: {user_id}, взял Isbn: {isbn}"
    
    def __check_by_3_books(self,user_id:int)->int:
        return len(self.users[user_id].borrowed_books)<3
    
    def return_book(self, user_id:int, isbn:int)->str:
        
        if isbn in self.books and user_id in self.users:
            borrowBook = self.books[isbn]
            user = self.users[user_id]
            borrowBook._return_book()
            user._return_book(borrowBook)
            self.__del_from_borrow_books(isbn)
            
            return f"Книга {isbn} возвращена"
        
        return self.BookNotFoundError()
    
    def __del_from_borrow_books(self,isbn):
        self.borrow_books.pop(isbn)
    
    def list_available_books(self)->dict:
        return {self.books[book].isbn:self.books[book].__dict__() for book in self.books
            if (self.books[book].is_borrowed == False)}
        
    def list_borrowed_books(self)->dict:
        return {self.borrow_books[book].isbn:self.borrow_books[book].__dict__() for book in self.borrow_books} ## long but working
    
    def search_books(self, title=None, author=None)->dict:
        return {self.books[book].isbn:self.books[book].__dict__() for book in self.books
                if (self.books[book].__dict__()['title'] == title or title is None) and
                (self.books[book].__dict__()['author'] == author or author is None)}

# lib = Library()

# print(lib.add_book("1984", "George Orwell", 1949, "001"))
# print(lib.add_book("King Arthur", "Merlin", 1927, "002"))
# print(lib.add_book("King Arthur", "Merlin", 1927, "002"))
# # print(lib.add_book("1984", "George", 1945, "ISBN-010"))
# print(lib.add_book("Alladin", "Allah", 1999, "003"))
# print(lib.add_book("Prince of Persia", "Unity", 2011, "004"))
# # print(lib.add_book("1984", "Merlin", 1927, "ISBN-005"))

# print(lib.add_user("Анна", 1))
# print(lib.add_user("Анна", 1))

# # print(lib.add_user("Kate", "user-2"))
# # print(lib.add_user("Kate", "user-2"))

# print(lib.borrow_book(1, "001"))
# print(lib.borrow_book(1, "002"))
# print(lib.borrow_book(1, "003"))
# print(lib.borrow_book(1, "004"))
# print(lib.return_book(1, "001"))
# print(lib.return_book(1, "002"))
# print(lib.return_book(1, "003"))

