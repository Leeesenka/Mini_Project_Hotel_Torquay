from django import forms

class DateForm(forms.Form):
    check_in_date = forms.DateField(widget=forms.SelectDateWidget())
    check_out_date = forms.DateField(widget=forms.SelectDateWidget())