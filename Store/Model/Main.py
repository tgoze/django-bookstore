from book_dao import BookDao

if __name__ == '__main__':
    
    book_dao = BookDao()
    
    for x in book_dao.searchBooks('b'):
        print(x.bookID, x.title, x.size, x.numberOfPages)

