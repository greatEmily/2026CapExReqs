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