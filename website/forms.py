from django import forms


class SearchForm(forms.Form):
    check_in_date = forms.DateField()
    check_out_date = forms.DateField()
    number_of_adults = forms.IntegerField()
    number_of_children = forms.IntegerField()
