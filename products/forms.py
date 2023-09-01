from django import forms
from .models import Comment, Contact_us


class CommentForms(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body', 'starts', ]


class ContactForms(forms.ModelForm):
    class Meta:
        model = Contact_us
        fields = ['name', 'email', 'phone_number', 'mesej',]

