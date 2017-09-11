""" forms.py """
from django import forms
from .models import Child, DailyRequirementsReport

class UpdateBlocksForm(forms.ModelForm):
    """ Form to update Child blocks """

    reason = forms.CharField(label='Reason for change', required=True)

    class Meta:
        model = Child
        fields = ('blocks',)

class UpdateDollarsForm(forms.ModelForm):
    """ Form to update Child dollars """

    reason = forms.CharField(label='Reason for change', required=True)
    add = forms.BooleanField(label='Add (not subtracting)', required=False)

    class Meta:
        model = Child
        fields = ('dollars',)

    def clean(self):
        """ override save method to optionally subtract """
        super(UpdateDollarsForm, self).clean()
        if not self.cleaned_data['add']:
            self.cleaned_data['dollars'] *= -1

class ScreentimePrereqsForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ScreentimePrereqsForm, self).__init__(*args, **kwargs)

    """ Form to create DailyRequirementsReport """
    class Meta:
        model = DailyRequirementsReport
        exclude = ('user',)
        widgets = {
            'reading_summary': forms.Textarea(attrs={'cols': 40, 'rows': 4}),
            'homework_description': forms.Textarea(attrs={'cols': 40, 'rows': 4}),
            'ixl_math_completed': forms.NumberInput(
                attrs={
                    'min': "0",
                    'max': "100",
                    'step': "1",
                    'value': "0",
                    'style': "width: 100px;",
                }),
            'ixl_language_arts_completed': forms.NumberInput(
                attrs={
                    'min': "0",
                    'max': "100",
                    'step': "1",
                    'value': "0",
                    'style': "width: 100px;",
                }),
        }

    
    
