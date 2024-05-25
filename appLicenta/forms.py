from django import forms

from appLicenta.models import User, Test


class PfpForm(forms.Form):
    image = forms.ImageField()


class ImageForm(forms.Form):
    image = forms.ImageField()
