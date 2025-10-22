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

    TYPE_CHOICES = [
        ('New Equipment', 'New Equipment'),
        ('Replacement', 'Replacement')
    ]

    type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Request Type'
    )

    approval_status = forms.CharField(
        initial='Requested',
        widget=forms.HiddenInput()
    )
    
    business_case = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Describe business case here for the equipemnt requested.',
            'rows': 4
        }),
        label='Business Case'
    ) 