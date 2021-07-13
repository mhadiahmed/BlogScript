from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import Author


class AuthorCreateForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model = Author
        fields = 'email','first_name','last_name','notification','role','status'
        
        
    def __init__(self, *args, **kwargs):
        super(AuthorCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'appearance-none block w-full py-3 px-4 leading-tight text-gray-700  focus:bg-white border border-gray-200 focus:border-gray-500 rounded focus:outline-none'

class AuthorEditForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Author
        fields = 'email','first_name','last_name','notification','role','status'
        exclude = ['password', 'confirm_password']
    
    def __init__(self, *args, **kwargs):
        super(AuthorEditForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'appearance-none block w-full py-3 px-4 leading-tight text-gray-700  focus:bg-white border border-gray-200 focus:border-gray-500 rounded focus:outline-none'
