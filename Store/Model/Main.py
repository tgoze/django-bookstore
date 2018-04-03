from book_dao import BookDao
from genre_dao import GenreDao
from genre import Genre

if __name__ == '__main__':
    
    g = GenreDao()
    for genre in g.get_all():
        print(genre.genre_id,genre.genre)
    
    

