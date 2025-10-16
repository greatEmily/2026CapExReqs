from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Fieldset, Submit
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
        labels = {
            'equipment': 'Equipment Type',
            'approval_status': 'Approval Status',
            'requisition_number': 'Requisition #',
            'po_number': 'PO #',
            'shipping_cost': 'Shipping Cost',
            'tax': 'Tax Amount',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Optional user for role-based logic
        super().__init__(*args, **kwargs)

        # Add custom styling or placeholders
        self.fields['equipment'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Select equipment'})
        self.fields['requisition_number'].widget.attrs.update({'placeholder': 'Enter requisition number'})
        self.fields['po_number'].widget.attrs.update({'placeholder': 'Enter PO number'})

        # Role-based field visibility (example: hide approval_status for non-managers)
        if user and not user.groups.filter(name='Managers').exists():
            self.fields['approval_status'].widget = forms.HiddenInput()

        # Crispy form helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Request Details',
                Row(
                    Column('equipment', css_class='form-group col-md-6 mb-0'),
                    Column('approval_status', css_class='form-group col-md-6 mb-0'),
                ),
                Row(
                    Column('requisition_number', css_class='form-group col-md-6 mb-0'),
                    Column('po_number', css_class='form-group col-md-6 mb-0'),
                ),
                Row(
                    Column('shipping_cost', css_class='form-group col-md-6 mb-0'),
                    Column('tax', css_class='form-group col-md-6 mb-0'),
                ),
            ),
            Submit('submit', 'Submit Request')
        )