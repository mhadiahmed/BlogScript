from site_settings.models import SiteSetting
from comments.forms import CommentForm
# from comments.models import Comment
from django.contrib import messages
# from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView
# from django.views.generic.edit import FormMixin
from posts.models import Categories, Post
from django_json_ld.views import JsonLdDetailView


class PostListViewFront(ListView):
    model = Post
    queryset = Post.objects.filter(status="active").order_by("-publish")#filter(status="active")
    template_name = "core/post_list.html"
    paginate_by = 6
    def get_context_data(self, **kwargs):
        context = super(PostListViewFront, self).get_context_data(**kwargs)
        sd = {
        "@context": "https://schema.org/",
        "@type": "WebSite",
        "name": "NETBLOG",
        "url": SiteSetting.objects.get(id=1).url,
        "potentialAction": {
            "@type": "SearchAction",
            "target": "{search_term_string}",
            "query-input": "required name=search_term_string"
            }
        }
        context.update({"featured":Post.objects.filter(featured=True,status="active")[:6],'sd':sd})
        return context


class CategoryPostListView(ListView):
    model = Post
    template_name = "core/post_list.html"
    
    def get_context_data(self, **kwargs):
        context = super(CategoryPostListView, self).get_context_data(**kwargs)
        context.update({"featured":Post.objects.filter(category=self.kwargs.get('pk'), status="active", featured=True)[:6]})
        return context

    def get_queryset(self):
        return Post.objects.filter(category=self.kwargs.get('pk'), status="active")


class PostDetailView(JsonLdDetailView,CreateView,DetailView):
    model = Post
    template_name = "core/post_detail.html"
    form_class = CommentForm
    lockup_field = 'slug'
    
    
    def get_success_url(self):
        messages.success(self.request,"Your comment is submitted to the admin will be visible soon")
        return reverse('core:detail', kwargs={"pk":self.object.id})
    
    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        category = Categories.objects.get(name=self.object.category.name)
        context["related_post"] = category.post_category.exclude(id=self.object.id)[:3]
        context["form"] = CommentForm(initial={"post":self.object})
        context["comments"] = self.object.post_comment.filter(status="approved")
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        form.save(commit=True)
        return super(PostDetailView, self).form_valid(form)
    