from django import forms
from .models import VideoUpload

class CarForm(forms.ModelForm):
    class Meta:
        model = VideoUpload
        fields = ['video']
        widgets = {
            'video' : forms.ClearableFileInput(attrs={'class':'form-control'}),
        }