class Book:

    def __init__(self):
        self.bookID = None
        self.isbn13 = None
        self.isbn10 = None
        self.title = None
        self.copyRightDate = None
        self.type = None
        self.edition = None
        self.numberOfPages = None
        self.image = None
        self.genre = None
        self.author = None
        self.publisher = None

    def get_bookID(self):
        return self.bookID

    def set_bookID(self,bookID):
        self.bookID=bookID

    def get_isbn13(self):
        return self.isbn13

    def set_isbn13(self,isbn13):
        self.isbn13=isbn13

    def get_isbn10(self):
        return self.isbn10

    def set_isbn10(self,isbn10):
        self.isbn10 = isbn10

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

    def get_copyRightDate(self):
        return self.copyRightDate

    def set_copyRightDate(self, copyRightDate):
        self.copyRightDate = copyRightDate

    def get_type(self):
        return self.type

    def set_type(self,type):
        self.type = type

    def get_edition(self):
        return self.edition

    def set_edition(self, edition):
        self.edition = edition

    def get_numberOfPages(self):
        return self.numberOfPages

    def set_numberOfPages(self,numberOfPages):
        self.numberOfPages = numberOfPages

    def get_image(self):
        return self.image

    def set_image(self, image):
        self.image = image

    def get_genre(self):
        return self.genre

    def set_genre(self,genre):
        self.genre = genre

    def get_author(self):
        return self.author

    def set_author(self,author):
        self.author = author

    def get_publisher(self):
        return self.publisher

    def set_publisher(self,publisher):
        self.publisher = publisher
