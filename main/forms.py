from django import forms
from .models import Comment

class AddComment(forms.ModelForm):
    # text = forms.CharField(
    #     label='Комментарий',
    #     required=True,
    #     min_length=5,
    #     widget=forms.Textarea(attrs={'placeholder': 'Введите сообщение'})
    # )
    
    class Meta:
        model = Comment
        fields = ['text', 'avtor', 'app']
        widgets = {'avtor': forms.HiddenInput(), 'app': forms.HiddenInput()}