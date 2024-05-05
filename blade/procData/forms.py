from django import forms

class uploadCSV(forms.Form):
	csv_file = forms.FileField(label='Upload CSV File')