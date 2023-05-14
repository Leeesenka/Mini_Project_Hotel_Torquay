from django import forms
from .models import Review


class DateForm(forms.Form):
    check_in_date = forms.DateField(widget=forms.SelectDateWidget())
    check_out_date = forms.DateField(widget=forms.SelectDateWidget())


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']    