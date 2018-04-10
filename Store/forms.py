from django import forms

from Store.Model.publisher_dao import PublisherDao
from Store.Model.genre_dao import GenreDao
from Store.Model.author_dao import AuthorDao

publisher_dao = PublisherDao()
genre_dao = GenreDao()
author_dao = AuthorDao()
publishers = []
for publisher in publisher_dao.get_all():
    publisher_val = (str(publisher.publisher_id), str(publisher.company_name))
    publishers.append(publisher_val)
genres = []
for genre in genre_dao.get_all():
    genre_val = (str(genre.genre_id), str(genre.genre))
    genres.append(genre_val)
authors = []
for author in author_dao.get_all():
    author_val = (str(author.author_id), str(author.last_name) + ", " + str(author.first_name))
    authors.append(author_val)

class BookForm(forms.Form):
    title = forms.CharField()
    authors = forms.ChoiceField(choices=authors)
    isbn10 = forms.CharField(max_length="10", min_length="10")
    isbn13 = forms.CharField(max_length="13", min_length="13")
    copyright_date = forms.DateField()
    edition = forms.DecimalField()
    publishers = forms.ChoiceField(choices=publishers)
    book_type = forms.CharField()
    num_pages = forms.IntegerField()
    genres = forms.ChoiceField(choices=genres)