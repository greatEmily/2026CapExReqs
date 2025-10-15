from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from .models import Request

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = [
            'equipment',
            'approval_status',
            'requisition_number',
            'po_number',
            'shipping_cost',
            'tax'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit Request'))