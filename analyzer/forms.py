from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()


class ChoiceForm(forms.Form):
    CHOICES = (
        (1, 'Processes vs Users'),
        (2, 'Process vs Time')
    )
    field = forms.ChoiceField(choices=CHOICES)




