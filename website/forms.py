from django.forms import ModelForm, Textarea, TextInput, Select, ClearableFileInput
from django.utils.translation import gettext_lazy as _
from . import models
from django import forms


class UploadBasetemp(ModelForm):
    class Meta:
        model = models.Base_template
        fields = ['modID', 'description', 'upload']
        widgets = {
            'modID': Select(attrs={
                'style': "margin-left: 38px;"
            }),
            'description': Textarea(attrs={
                    'id': 'text-area-2',
                    'class': "form-control",
                    'rows': "7",
                    'placeholder': "Placeholder text.",
                    'style': 'margin-bottom: 20px;'
            }),
            'upload': ClearableFileInput(attrs={
                'style': "margin-left: 35px;"
            })
        }
        labels = {
            'name': _('File name'),
            'modID': _('Model')
        }


class addConfig(forms.Form):
    console_pass = forms.CharField(
        label='Console Password',
        widget=forms.TextInput(attrs={
            'class': "col-md-10",
            'style': "margin-left: 30px; margin-right: 30px; margin-bottom: 20px; padding-left: 5px",
            'type': 'password'
        }),
        required=False,

    )
    enable_pass = forms.CharField(
        label='Enable Password',
        widget=forms.TextInput(attrs={
            'class': "col-md-10",
            'style': "margin-left: 40px; margin-right: 30px; margin-bottom: 20px; padding-left: 5px",
            'type': 'password'
        }),
        required=False
    )
    script = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': "col-md-11",
            'rows': "20",
            'placeholder': "text.",
            'style': "padding-left: 10px;padding-top: 5px;padding-bottom: 0px; margin-left: 30px; margin-bottom: 20px;"

        }),
        required=False
    )
    upload = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
            'style': "margin-left: 22px;"
        }),
        required=False
    )


class cmd(forms.Form):
    data_in = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': "col-lg-11 data_out",
            'placeholder': "Enter your command.",
            'style': "padding-left: 10px; margin: 10px 20px 2px 30px;"
        }),
        required=False
    )