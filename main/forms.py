from django import forms
from django.core.exceptions import ValidationError
import re

class FinancialDataForm(forms.Form):
    EQUITY_ERROR_MESSAGE = "Equity must be in uppercase letters."
    YEAR_ERROR_MESSAGE = "Year must be in YYYY format with all numbers or empty."
    DATE_ERROR_MESSAGE = "Date must be in YYYY-MM-DD format."
    PDF_ERROR_MESSAGE = "Please upload a valid PDF file."

    QUARTER_CHOICES = [('', 'None'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')]

    equity = forms.CharField(max_length=100, error_messages={'required': EQUITY_ERROR_MESSAGE})
    quarter = forms.ChoiceField(choices=QUARTER_CHOICES, required=False)
    year = forms.CharField(max_length=4, required=False, error_messages={'invalid': YEAR_ERROR_MESSAGE})
    published_date = forms.DateField(input_formats=['%Y-%m-%d'], error_messages={'invalid': DATE_ERROR_MESSAGE})
    fiscal_date = forms.DateField(input_formats=['%Y-%m-%d'], required=False, error_messages={'invalid': DATE_ERROR_MESSAGE})
    file = forms.FileField(error_messages={'invalid': PDF_ERROR_MESSAGE})

    def clean_equity(self):
        equity = self.cleaned_data.get('equity')
        if equity != equity.upper():
            raise ValidationError(self.EQUITY_ERROR_MESSAGE)
        return equity

    def clean_year(self):
        year = self.cleaned_data.get('year')
        if year and not re.fullmatch(r'^\d{4}$', year):
            raise ValidationError(self.YEAR_ERROR_MESSAGE)
        return year

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            file_type = file.content_type
            if file_type != 'application/pdf':
                raise ValidationError(self.PDF_ERROR_MESSAGE)
        return file


from django import forms
from django.core.exceptions import ValidationError
import re

class ContentForm(forms.Form):
    EQUITY_ERROR_MESSAGE = "Equity must be in uppercase letters."
    DATE_ERROR_MESSAGE = "Date must be in YYYY-MM-DD format."
    PDF_ERROR_MESSAGE = "Please upload a valid PDF file."

    CONTENT_TYPE_CHOICES = [
        ('sellside_conference_presentation', 'Sellside Conference Presentation'),
        ('sellside_conference_transcript', 'Sellside Conference Transcript'),
        ('sellside_conference_other', 'Sellside Conference Other'),
        ('company_conference_presentation', 'Company Conference Presentation'),
        ('company_conference_transcript', 'Company Conference Transcript'),
        ('company_conference_other', 'Company Conference Other'),
        ('industry_conference_presentation', 'Industry Conference Presentation'),
        ('industry_conference_transcript', 'Industry Conference Transcript'),
        ('industry_conference_other', 'Industry Conference Other'),
        ('other', 'Other'),
    ]

    equity = forms.CharField(max_length=100, error_messages={'required': EQUITY_ERROR_MESSAGE})
    content_name = forms.CharField(max_length=100)
    content_type = forms.ChoiceField(choices=CONTENT_TYPE_CHOICES)
    published_date = forms.DateField(input_formats=['%Y-%m-%d'], error_messages={'invalid': DATE_ERROR_MESSAGE})
    file = forms.FileField(error_messages={'invalid': PDF_ERROR_MESSAGE})

    def clean_equity(self):
        equity = self.cleaned_data.get('equity')
        if equity != equity.upper():
            raise ValidationError(self.EQUITY_ERROR_MESSAGE)
        return equity

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            file_type = file.content_type
            if file_type != 'application/pdf':
                raise ValidationError(self.PDF_ERROR_MESSAGE)
        return file
