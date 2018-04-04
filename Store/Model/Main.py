from author_dao import AuthorDao
from author import Author

if __name__ == '__main__':
    
    author_dao = AuthorDao()
    
    # author = Author()
    # author.author_id = 11
    # author.first_name = "George"
    # author.last_name = "Smith"
    # author_dao.update(author)

    # for x in author_dao.get_all():
    #     print(x.author_id, x.first_name, x.last_name)

    author_dao.delete(11)