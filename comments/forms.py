from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    # post = 
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body','post')
        # fields['post'].widget.atters['type'] = "hidden"
        
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['post'].widget = forms.HiddenInput()
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
