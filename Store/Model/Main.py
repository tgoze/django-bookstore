from Store.Model import book, bookdao
if __name__ == '__main__':

    for x in bookdao.searchBooks('b'):
        print(x.bookID, x.title, x.size, x.numberOfPages)

