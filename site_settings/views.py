from typing import Any
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.urls.base import reverse_lazy
from django.views.generic import UpdateView, CreateView, DeleteView, ListView
from .models import SiteSetting, Option
from .forms import CategoriesForm, OptionForm, SiteSettingForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from authors.decorators import allowed_users
from posts.models import Categories
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q

@method_decorator(login_required, name="dispatch")
@method_decorator(allowed_users(allowed_roles=['admin']), name="dispatch")
class SiteSettingsListView(UpdateView):
    model = SiteSetting
    form_class = SiteSettingForm
    success_url = "/settings/1"
    def get_object(self, queryset=None):
        obj, created = SiteSetting.objects.get_or_create(**self.kwargs)
        if obj:
            obj.author = self.request.user
            obj.save()
        return obj
    

@method_decorator(login_required, name="dispatch")
@method_decorator(allowed_users(allowed_roles=['admin']), name="dispatch")
class SiteOption(UpdateView): 
    model = Option
    form_class = OptionForm
    success_url = "/settings/options/1"
    def get_object(self, queryset=None):
        obj, created = Option.objects.get_or_create(**self.kwargs)
        if obj:
            obj.author = self.request.user
            obj.save()
        return obj


"""
    Category Model: CRUD Views
"""

class CategoryListView(ListView):
    model = Categories
    template_name = "site_settings/categories_list.html"
    # queryset = Categories.objects.all()
    # paginate_by = 15
    
    def get_queryset(self):
        qs = super(CategoryListView, self).get_queryset()
        post_filter = self.request.GET.get('post_filter')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(name__icontains=q))
        if post_filter and post_filter != "all":
            qs = qs.filter(status=post_filter)
        return qs


class CreateUpdateMixin(CreateView):
    model = Categories
    form_class = CategoriesForm
    template_name = "site_settings/categories_form.html"


class CategoryCreateView(CreateUpdateMixin):
    def form_valid(self, form):
        form.save(commit=True)
        messages.success(self.request, "Category have been added successfully.")
        return redirect(reverse('settings:list'))


class CategoryUpdateView(CreateUpdateMixin, UpdateView):
    def form_valid(self, form):
        form.save(commit=True)
        messages.success(self.request, "Category have been updated successfully.")
        return redirect(reverse('settings:list'))


class CategoryDeleteView(DeleteView):
    model = Categories
    template_name = 'site_settings/categories_confirm_delete.html'
    success_url = reverse_lazy('settings:list')
    context_object_name = "category"
    
    def delete(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        messages.success(self.request, 'Category deleted successfully')
        return super().delete(request, *args, **kwargs)