from django import forms

class UploadCsvfile(forms.Form):
    csvFileField= forms.FileField(label='file', error_messages = {'required': 'File required'})
