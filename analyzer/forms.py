from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()

choices_dict = {'1': 'time', '2': 'Usr', '3': "processName", '4': 'process',
           '5': 'OSThread', '6': 'clientID', '7': 'applicationName', '8': 'computerName',
           '9': 'connectID', '10': 'SessionID', '11': 'Trans', '12': 'dbpid',
           '13': 'Sql', '14': 'Rows', '15': 'planSQLText', '16': 'Context'}


class ChoiceForm(forms.Form):
    CHOICES = tuple([(i, f'Processes vs {choices_dict[str(i)]}') for i in range(1, 17)])

    field = forms.ChoiceField(choices=CHOICES)




