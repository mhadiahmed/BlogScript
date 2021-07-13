from django import forms
from .models import SiteSetting, Option
from posts.models import Categories

class SiteSettingForm(forms.ModelForm):
    """Form definition for SiteSetting."""

    class Meta:
        """Meta definition for SiteSettingform."""

        model = SiteSetting
        fields = ('name','description','url')
    
    def __init__(self, *args, **kwargs):
        super(SiteSettingForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'appearance-none block w-full py-3 px-4 leading-tight text-gray-700  focus:bg-white border border-gray-200 focus:border-gray-500 rounded focus:outline-none'

class OptionForm(forms.ModelForm):
    """Form definition for Option."""
    
    class Meta:
        """Meta definition for Optionform."""

        model = Option
        fields = "__all__"
        exclude = ['id','author']
        
    def __init__(self, *args, **kwargs):
        super(OptionForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'appearance-none block w-full py-3 px-4 leading-tight text-gray-700  focus:bg-white border border-gray-200 focus:border-gray-500 rounded focus:outline-none'



class CategoriesForm(forms.ModelForm):
    """Form definition for Categories."""

    class Meta:
        """Meta definition for Categoriesform."""

        model = Categories
        fields = "__all__"
        exclude = ['id']

    def __init__(self, *args, **kwargs):
        super(CategoriesForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'appearance-none block w-full py-3 px-4 leading-tight text-gray-700  focus:bg-white border border-gray-200 focus:border-gray-500 rounded focus:outline-none'