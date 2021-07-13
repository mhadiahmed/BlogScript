from django.contrib import messages
from django.shortcuts import redirect  # , render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.db.models import Q
from .forms import PostDashboardModelForm
# from django_filters import filters
from .models import Post  # Categories,

# from .filters import PostFilter


class PostListView(ListView):
    model = Post
    template_name = "posts/posts.html"
    queryset = Post.objects.all().order_by('-publish')
    paginate_by = 15
    
    def get_queryset(self):
        qs = super(PostListView, self).get_queryset()
        post_filter = self.request.GET.get('post_filter')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(body__icontains=q))

        if post_filter and post_filter != "all":
            qs = qs.filter(status=post_filter).order_by('-publish')
        return qs


class CreateUpdateMixin(CreateView):
    model = Post
    form_class = PostDashboardModelForm
    template_name = "posts/add_post.html"


class PostCreateView(CreateUpdateMixin):
    def form_valid(self, form):
        form.save(commit=True)
        messages.success(self.request, "Post have been added successfully.")
        return redirect(reverse('posts:list'))


class PostUpdateView(CreateUpdateMixin, UpdateView):
    def form_valid(self, form):
        form.save(commit=True)
        messages.success(self.request, "Post have been updated successfully.")
        return redirect(reverse('posts:list'))


class PostDeleteView(DeleteView):
    model = Post
    success_url = "/posts/"
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Post deleted successfully")
        return super(PostDeleteView, self).delete(request, *args, **kwargs)

