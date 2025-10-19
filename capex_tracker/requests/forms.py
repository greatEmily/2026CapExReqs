from django import forms
from.models import Equipment

class RequestForm(forms.Form):
    equipment = forms.ModelChoiceField(
        queryset=Equipment.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    approval_status = forms.CharField(
        initial='Requested',
        widget=forms.HiddenInput()
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Describe the business case and whether this is a replacement or new equipment request',
            'rows': 4
        }),
        label='Request Notes'
    )