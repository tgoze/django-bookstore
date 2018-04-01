from Store.Model import book, bookdao
if __name__ == '__main__':
    z = book.Book()
    z.set_bookID(469249)
    z.set_isbn13(9999999999979)
    z.set_isbn10(3333333733)
    z.set_title('Bed')
    z.set_copyRightDate("2018-03-28")
    z.set_type('paperBack')
    z.set_edition(9)
    z.set_numberOfPages(503)
    z.set_size(9)
    z.set_weight(8)
    z.set_image('image5')
    z.set_genre(31)
    z.set_authorID(11)
    z.set_publisherID(53)
    bookdao.updateBook(z)
    for x in bookdao.getAllBooks():
        print(x.bookID, x.title, x.size, x.numberOfPages)

