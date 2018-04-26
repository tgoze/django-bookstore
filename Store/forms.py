from django import forms
from django.forms.widgets import Select
from localflavor.us.forms import *
from localflavor.us.us_states import *

from Store.Model.publisher_dao import PublisherDao
from Store.Model.genre_dao import GenreDao
from Store.Model.author_dao import AuthorDao

# This gets all of the choices for the select elements
# It also adds a default option which is disabled
states = []
states.append(("default", {'label': "Choose a state", 'disabled': True}))
for state in CONTIGUOUS_STATES:
    states.append(state)

address_types = []
address_types.append(("default", {'label': "Choose an address type", 'disabled': True}))
address_types.append(('Billing','Billing'))
address_types.append(('Shipping','Shipping'))



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
    def __init__(self, *args, **kwargs):
        author_choices = kwargs.pop('author_choices')
        publisher_choices = kwargs.pop('publisher_choices')
        genre_choices = kwargs.pop('genre_choices')
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['authors'] = forms.ChoiceField(choices=author_choices, initial="default", widget=SelectWithDisabled())
        self.fields['publishers'] = forms.ChoiceField(choices=publisher_choices, initial="default", widget=SelectWithDisabled())
        self.fields['genres'] = forms.ChoiceField(choices=genre_choices, initial="default", widget=SelectWithDisabled())

    title = forms.CharField()
    authors = forms.ChoiceField()
    isbn10 = forms.CharField(max_length="10", min_length="10")
    isbn13 = forms.CharField(max_length="13", min_length="13")
    copyright_date = forms.DateField()
    edition = forms.DecimalField()
    publishers = forms.ChoiceField()
    book_type = forms.CharField()
    num_pages = forms.IntegerField()
    genres = forms.ChoiceField()
    quantity_on_hand = forms.IntegerField()
    cost = forms.DecimalField(help_text="In US dollars")
    retail_price = forms.DecimalField(help_text="In US dollars")

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
    phone_number = forms.CharField(max_length="10", min_length="10")
    contact_name = forms.CharField()

class GenreForm(forms.Form):
    genre = forms.CharField()

class GenreForm2(forms.Form):
    genre_id = forms.CharField()
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
    home_phone = forms.CharField(max_length="10", min_length="10")
    work_phone = forms.CharField(max_length="10", min_length="10")
    

class CustomerInfoForm(forms.Form):
    home_phone = forms.CharField(max_length="10", min_length="10")
    work_phone = forms.CharField(max_length="10", min_length="10")
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()


class DeleteAddressForm(forms.Form):
    address_id = forms.CharField()


class AddAddressForm(forms.Form):
    street = forms.CharField()
    city = forms.CharField()
    state_code = forms.ChoiceField(choices=states, initial="default", widget=SelectWithDisabled())
    zip_code = USZipCodeField()
    address_type = forms.ChoiceField(choices=address_types, initial="default", widget=SelectWithDisabled())


class AddAddressForm2(forms.Form):
    street = forms.CharField()
    city = forms.CharField()
    state_code = forms.ChoiceField(choices=states, initial="default", widget=SelectWithDisabled())
    zip_code = USZipCodeField()


class EditAddressForm(forms.Form):
    street = forms.CharField()
    city = forms.CharField()
    state_code = forms.ChoiceField(choices=states, initial="default", widget=SelectWithDisabled())
    zip_code = USZipCodeField()
    address_type = forms.ChoiceField(choices=address_types, initial="default", widget=SelectWithDisabled())
    
class AddPaymentInfoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        bill_address_choices = kwargs.pop('bill_address_choices')
        super(AddPaymentInfoForm, self).__init__(*args, **kwargs)
        self.fields['billing_addresses'] = forms.ChoiceField(widget=forms.RadioSelect, choices=bill_address_choices)
    
    card_number = forms.CharField(max_length="16", min_length="16")
    cvc = forms.CharField(max_length="3", min_length="3", widget=forms.PasswordInput)
    expir_date = forms.DateField()
    card_issuer = forms.CharField()
    billing_addresses = forms.ChoiceField()



class AddPaymentInfoForm2(forms.Form):
    card_number = forms.CharField(max_length="16", min_length="16")
    cvc = forms.CharField(max_length="3", min_length="3", widget=forms.PasswordInput)
    expir_date = forms.DateField()
    card_issuer = forms.CharField()
    


class ChangeUsernamePassword(forms.Form):
    username = forms.CharField()
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=32, widget=forms.PasswordInput)


class OrderForm(forms.Form):
    quantity_ordered = forms.IntegerField()


class CartForm(forms.Form):
    def __init__(self, max_quantity, *args, **kwargs):
        super(CartForm, self).__init__(*args, **kwargs)
        self.fields['quantity_ordered'] = forms.IntegerField(max_value=max_quantity)

    quantity_ordered = forms.IntegerField(max_value=None)


class ShipPayForm(forms.Form):
    def __init__(self, *args, **kwargs):
        card_choices = kwargs.pop('card_choices')
        shipping_choices = kwargs.pop('shipping_choices')
        super(ShipPayForm, self).__init__(*args, **kwargs)
        self.fields['credit_cards'] = forms.ChoiceField(widget=forms.RadioSelect, choices=card_choices)
        self.fields['shipping_addresses'] = forms.ChoiceField(widget=forms.RadioSelect, choices=shipping_choices)

    credit_cards = forms.ChoiceField()
    shipping_addresses = forms.ChoiceField()
