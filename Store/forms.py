from django import forms
from django.forms.widgets import Select
from localflavor.us.forms import *
from localflavor.us.us_states import *

from Store.Model.publisher_dao import PublisherDao
from Store.Model.genre_dao import GenreDao
from Store.Model.author_dao import AuthorDao

publisher_dao = PublisherDao()
genre_dao = GenreDao()
author_dao = AuthorDao()

# This gets all of the choices for the select elements
# It also adds a default option which is disabled
authors = []
authors.append(("default", {'label': "Choose an author", 'disabled': True}))
for author in author_dao.get_all():
    author_val = (str(author.author_id), str(author.last_name) + ", " + str(author.first_name))
    authors.append(author_val)
publishers = []
publishers.append(("default", {'label': "Choose a publisher", 'disabled': True}))
for publisher in publisher_dao.get_all():
    publisher_val = (str(publisher.publisher_id), str(publisher.company_name))
    publishers.append(publisher_val)
genres = []
genres.append(("default", {'label': "Choose a genre", 'disabled': True}))
for genre in genre_dao.get_all():
    genre_val = (str(genre.genre_id), str(genre.genre))
    genres.append(genre_val)
states = []
states.append(("default", {'label': "Choose a state", 'disabled': True}))
for state in CONTIGUOUS_STATES:
    states.append(state)

# https://djangosnippets.org/snippets/2453/
class SelectWithDisabled(Select):
    """
    Subclass of Django's select widget that allows disabling options.
    To disable an option, pass a dict instead of a string for its label,
    of the form: {'label': 'option label', 'disabled': True}
    """

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        disabled = False
        if isinstance(label, dict):
            label, disabled = label['label'], label['disabled']
        option_dict = super(SelectWithDisabled, self).create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
        if disabled:
            option_dict['attrs']['disabled'] = 'disabled selected'
        return option_dict


class BookForm(forms.Form):
    title = forms.CharField()
    authors = forms.ChoiceField(choices=authors, initial="default", widget=SelectWithDisabled())
    isbn10 = forms.CharField(max_length="10", min_length="10")
    isbn13 = forms.CharField(max_length="13", min_length="13")
    copyright_date = forms.DateField()
    edition = forms.DecimalField()
    publishers = forms.ChoiceField(choices=publishers, initial="default", widget=SelectWithDisabled())
    book_type = forms.CharField()
    num_pages = forms.IntegerField()
    genres = forms.ChoiceField(choices=genres, initial="default", widget=SelectWithDisabled())


class BookImageForm(forms.Form):
    image = forms.ImageField()


class AuthorForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()


class PublisherForm(forms.Form):
    company_name = forms.CharField()
    city = forms.CharField()
    state_code = forms.ChoiceField(choices=states, initial="default", widget=SelectWithDisabled())
    zip_code = USZipCodeField()


class GenreForm(forms.Form):
    genre = forms.CharField()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)


class RegisterUserForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    

class CartForm(forms.Form):
    def __init__(self, max_quantity, *args, **kwargs):
        super(CartForm, self).__init__(*args, **kwargs)
        self.fields['quantity_ordered'] = forms.IntegerField(max_value=max_quantity)

    quantity_ordered = forms.IntegerField(max_value=None)


class ShipPayForm(forms.Form):
    def __init__(self, card_choices, shipping_choices, *args, **kwargs):
        super(ShipPayForm, self).__init__(*args, **kwargs)
        self.fields['credit_cards'] = forms.ChoiceField(widget=forms.RadioSelect, choices=card_choices)
        self.fields['shipping_addresses'] = forms.ChoiceField(widget=forms.RadioSelect, choices=shipping_choices)

    credit_cards = forms.ChoiceField()
    shipping_addresses = forms.ChoiceField()