from django import forms
from .models import Question
from .models import Comment


class QuestionForm(forms.ModelForm):
    class Meta: 
        model= Question
        fields = ('title','content')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'content']

        widgets = {
            'name': forms.TextInput(attrs ={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }
