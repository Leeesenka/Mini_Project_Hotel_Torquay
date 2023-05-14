from django import forms
from .models import Booking, User, Review
from django.core.validators import MinValueValidator


class DateForm(forms.Form):
    check_in_date = forms.DateField(widget=forms.SelectDateWidget())
    check_out_date = forms.DateField(widget=forms.SelectDateWidget())
    
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
        widgets = {
            'check_in_date': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}), 
            'check_out_date': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}
            )}

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']    