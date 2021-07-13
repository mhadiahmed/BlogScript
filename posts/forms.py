from django import forms
from .models import Post
from ckeditor.fields import RichTextField

class PostDashboardModelForm(forms.ModelForm):
    # body = RichTextField()
    class Meta:
        model = Post
        fields = ["author", "category", "title", "body", "image", "status",'meta_tag_title','meta_tag_description','meta_tag_keywords']
        
    
    def __init__(self, *args, **kwargs):
        super(PostDashboardModelForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'appearance-none block w-full py-3 px-4 leading-tight text-gray-700  focus:bg-white border border-gray-200 focus:border-gray-500 rounded focus:outline-none'



# class PostModelForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ""