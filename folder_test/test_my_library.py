import pytest
import my_library.my_library as liba

@pytest.fixture
def library_with_books()->object:
    lib = liba.Library()
    books = [
        ("King Arthur", "Merlin", 1927, "ISBN-002"),
        ("1984", "George Orwell", 1949, "ISBN-001"),
        ("Alladin", "Allah", 1999, "ISBN-003"),
        ("Prince of Persia", "Unity", 2011, "ISBN-004"),
        ("1984", "George", 1945, "ISBN-010")
    ]
    for title, author, year, isbn in books:
        lib.add_book(title, author, year, isbn)
    return lib

@pytest.fixture
def library_with_user(library_with_books:object)->object:
    library_with_books.add_user("Анна","user-1")
    return library_with_books

def test_add_book(library_with_books:object)->object:
    result = library_with_books.add_book("New Book", "Author", 2023, "ISBN-005")
    assert result == "Книга добавлена"
    
def test_add_user(library_with_books:object)->object:
    result = library_with_books.add_user("Иван","user-2")
    assert result == "Пользователь добавлен"  
    
def test_list_borrowed_books(library_with_books:object)->object:
    result = library_with_books.list_borrowed_books()
    return result

def test_borrow_book(library_with_user:object)->str:
    result = library_with_user.borrow_book("user-1","ISBN-001")
    assert result == "user-1 взял ISBN-001"

def test_search_books(library_with_books:object)->str:
    result = library_with_books.search_books("1984")
    assert result == ['1984, George Orwell, 1949, ISBN: ISBN-001', '1984, George, 1945, ISBN: ISBN-010']

def test_borrow_book1(library_with_user:object)->str:
    result = library_with_user.borrow()
    assert result == "user-1 взял ISBN-001"
# Зависит от реализации
# import pytest

# import my_library.my_library as lib

# @pytest.mark.parametrize("values1, values2, values3, values4, expected_result",[
#     ("1984", "George Orwell", 1949, "ISBN-001", "Книга добавлена"),
# ])
# def testLibraryaddbook(values1,values2,values3,values4,expected_result):
#     test = lib.Library()
#     test = test.add_book(values1,values2,values3,values4)
#     assert test == expected_result

# @pytest.mark.parametrize("values1, values2, expected_result",[
#     ("Анна", "user-1", "Пользователь добавлен"),
# ])
# def testLibraryadduser(values1,values2,expected_result):
#     test = lib.Library()
#     test_add_user = test.add_user(values1,values2)
        
#     assert test_add_user == expected_result
    
# @pytest.mark.parametrize("values1, values2, values3, values4, expected_result",[
#     ("1984", "George Orwell", 1949, "ISBN-001", ['1984, George Orwell, 1949, ISBN: ISBN-001'])
# ])
# def testLibraryshowallboks(values1,values2,values3,values4,expected_result):
#     test = lib.Library()
#     test.add_book(values1,values2,values3,values4)
#     test_available_books = test.list_available_books()
#     assert test_available_books == expected_result
    
# @pytest.mark.parametrize("value,expected_value,values1, values2, values3, values4, values5, values6, values7,values8, expected_result1,expected_result2,expected_result3",[
#     ([("King Arthur", "Merlin", 1927, "ISBN-002"),
#       ("1984", "George Orwell", 1949, "ISBN-001"),
#       ("Alladin", "Allah", 1999, "ISBN-003"),
#       ("Prince of Persia", "Unity", 2011, "ISBN-004")
#       ],
#      "Книга добавлена",
#     "1984", 
#      "George Orwell", 
#      1949, 
#      "ISBN-001", 
#      "user-1",
#      "Анна",
#      "user-0",
#      "ISBN-0",
#      "user-1 взял 1984, George Orwell, 1949, ISBN: ISBN-001",
#      "User не найден...",
#      "Книга не найдена...")
# ])
# def testBorrowBook(value,expected_value,values1,values2,values3,values4,values5,values6,values7, values8,expected_result1,expected_result2,expected_result3):
#     test = lib.Library()
#     test.add_user(values6,values5)
#     for element in value:
#         assert test.add_book(element[0],element[1],element[2],element[3])== expected_value
#         test_borrow_book = test.borrow_book(values5,element[3])
    
    
#     test_user_not_in_library = test.borrow_book(values7,values4)
#     test_book_not_in_library = test.borrow_book(values5,values8)
    
#     assert test_borrow_book == expected_result1
#     assert test_user_not_in_library == expected_result2
#     assert test_book_not_in_library == expected_result3