from django import forms
from.models import Equipment, Type

class RequestForm(forms.Form):
    name = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Requester Name',
            'rows': 1
        }),
        label='Requester Name'
    ) 
    equipment = forms.ModelChoiceField(
        queryset=Equipment.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    type = forms.ModelChoiceField(
        queryset=Type.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    approval_status = forms.CharField(
        initial='Requested',
        widget=forms.HiddenInput()
    )
