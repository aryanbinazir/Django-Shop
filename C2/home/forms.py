from django import forms
from django.forms.widgets import Textarea
from .models import Comment

class CommentAddForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {'body':Textarea(attrs={'class':'form-control'})}
