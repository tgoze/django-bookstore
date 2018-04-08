from django import forms

class BookForm(forms.Form):
    title = forms.CharField()
