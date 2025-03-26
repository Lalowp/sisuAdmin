from django import forms

from sisu.models import Guest


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(required=False)

class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['name', 'cellphone', 'invitations', 'assists', 'extraGuests']