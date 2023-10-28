from django import forms

class ConversionForm(forms.Form):
    source_base = forms.IntegerField(label='Source Base')
    target_base = forms.IntegerField(label='Target Base')
    input_number = forms.CharField(label='Input Number')
