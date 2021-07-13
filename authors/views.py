# from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.api import get_messages
from authors.decorators import allowed_users
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, render
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView, ListView, UpdateView
from django.db.models import Q
from .forms import AuthorCreateForm, AuthorEditForm
from .models import Author

@method_decorator(login_required, name="dispatch")
@method_decorator(allowed_users(allowed_roles=['admin']), name="dispatch")
class AuthorListView(ListView):
    model = Author
    template_name = "authors/authors.html"
    def get_queryset(self):
        qs = super(AuthorListView, self).get_queryset()
        post_filter = self.request.GET.get('post_filter')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q))
        if post_filter and post_filter != "all":
            qs = qs.filter(status=post_filter)
        return qs

@method_decorator(login_required, name="dispatch")
@method_decorator(allowed_users(allowed_roles=['admin']), name="dispatch")
class AuthorEditView(UpdateView):
    model = Author
    form_class = AuthorEditForm
    template_name = "authors/add_author.html"
    slug_field = 'pk'
    def form_valid(self, form):
        form.save(commit=True)
        messages.success(self.request,"author was updated successfully.")
        return redirect(reverse('authors:authors'))

@method_decorator(login_required, name="dispatch")
@method_decorator(allowed_users(allowed_roles=['admin']), name="dispatch")
class AuthorDeleteView(DeleteView):
    model = Author
    success_url = reverse_lazy("authors:authors")
    
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "author was deleted successfully.")
        return super(AuthorDeleteView,self).delete(request, *args, **kwargs)



@login_required()
@allowed_users(allowed_roles=['admin'])
def add_author(request):
    if request.method == "POST":
        form = AuthorCreateForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.first_name.lower()
            user.save()
            print("data saved.")
            messages.success(request,"author add successfully.")
            return redirect("dashboard")
    else:
        form = AuthorCreateForm()
        return render(request, 'authors/add_author.html',{'form':form})


class PasswordResetView(auth_views.PasswordResetView):
    template_name = "registration/password_reset_form.html"
    success_url = reverse_lazy('authors:password_reset_done')


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    success_url = reverse_lazy("authors:password_reset_complete")
