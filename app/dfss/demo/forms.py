from django import forms


class ResumeForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )
