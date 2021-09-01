from django import forms

from main.models import Contract


class TemplateUploadForm(forms.ModelForm):

    class Meta:
        model = Contract
        fields = ['template_of_contract', 'amount', 'status', 'type', 'company', 'name']