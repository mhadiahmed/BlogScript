from typing import Any

from authors.decorators import allowed_users
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template import loader
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from posts.models import Categories

from site_settings.utils import TEMPLATE_PATH

from .forms import CategoriesForm, OptionForm, PageForm, SiteSettingForm
from .models import Option, Page, SiteSetting


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
@method_decorator(login_required, name="dispatch")
@method_decorator(allowed_users(allowed_roles=['admin']), name="dispatch")
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

@method_decorator(login_required, name="dispatch")
@method_decorator(allowed_users(allowed_roles=['admin']), name="dispatch")
class CategoryCreateView(CreateUpdateMixin):
    def form_valid(self, form):
        form.save(commit=True)
        messages.success(self.request, "Category have been added successfully.")
        return redirect(reverse('settings:list'))


@method_decorator(login_required, name="dispatch")
@method_decorator(allowed_users(allowed_roles=['admin']), name="dispatch")
class CategoryUpdateView(CreateUpdateMixin, UpdateView):
    def form_valid(self, form):
        form.save(commit=True)
        messages.success(self.request, "Category have been updated successfully.")
        return redirect(reverse('settings:list'))

@method_decorator(login_required, name="dispatch")
@method_decorator(allowed_users(allowed_roles=['admin']), name="dispatch")
class CategoryDeleteView(DeleteView):
    model = Categories
    template_name = 'site_settings/categories_confirm_delete.html'
    success_url = reverse_lazy('settings:list')
    context_object_name = "category"
    
    def delete(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        messages.success(self.request, 'Category deleted successfully')
        return super().delete(request, *args, **kwargs)
    

@method_decorator(login_required, name="dispatch")
@method_decorator(allowed_users(allowed_roles=['admin']), name="dispatch")
class PageListView(ListView):
    model = Page
    template_name = "site_settings/page_list.html"
    
    def get_queryset(self):
        qs = super(PageListView, self).get_queryset()
        post_filter = self.request.GET.get('post_filter')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(title__icontains=q))
        if post_filter and post_filter != "all":
            qs = qs.filter(status=post_filter)
        return qs

@method_decorator(login_required, name="dispatch")
@method_decorator(allowed_users(allowed_roles=['admin']), name="dispatch")
class PageCreateView(CreateView):
    model = Page
    form_class = PageForm
    # template_name = "site_settings/page_form.html"
    
@method_decorator(login_required, name="dispatch")
@method_decorator(allowed_users(allowed_roles=['admin']), name="dispatch")    
class PageUpdateView(UpdateView):
    model = Page
    form_class = PageForm
    # template_name = "site_settings/"

@method_decorator(login_required, name="dispatch")
@method_decorator(allowed_users(allowed_roles=['admin']), name="dispatch")
class PageDeleteView(DeleteView):
    model = Page
    template_name = 'site_settings/page_confirm_delete.html'
    success_url = reverse_lazy('settings:page_list')
    context_object_name = "page"
    
    def delete(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        messages.success(self.request, 'Page deleted successfully')
        return super().delete(request, *args, **kwargs)
    

DEFAULT_TEMPLATE = 'core/default.html'


def page(request, url):
    if not url.startswith('/'):
        url = '/' + url
    site_id = get_current_site(request).id
    try:
        f = get_object_or_404(Page, url=url, sites=site_id)
    except Http404:
        if not url.endswith('/') and settings.APPEND_SLASH:
            url += '/'
            f = get_object_or_404(Page, url=url, sites=site_id)
            return HttpResponsePermanentRedirect('%s/' % request.path)
        else:
            raise
    return render_page(request, f)


@csrf_protect
def render_page(request, f):
    
    """
    Internal interface to the flat page view.
    """
    # If registration is required for accessing this page, and the user isn't
    # logged in, redirect to the login page.
    if f.registration_required and not request.user.is_authenticated:
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.path)
    if f.template_name:
        template = loader.select_template((f"{TEMPLATE_PATH}{f.template_name}", DEFAULT_TEMPLATE))
    else:
        template = loader.get_template(DEFAULT_TEMPLATE)

    f.title = mark_safe(f.title)
    f.content = mark_safe(f.content)

    return HttpResponse(template.render({'pages': f}, request))
