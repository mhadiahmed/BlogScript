from site_settings.models import SiteSetting
from django.shortcuts import render
from django.template import context
from authors.decorators import allowed_users
from posts.models import Post
from authors.models import Author
from comments.models import Comment
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.admin.models import LogEntry

@login_required()
@allowed_users(allowed_roles=['admin','author'])
def dashboard(request):
    post_count = Post.objects.all().count()
    author_count = Author.objects.filter(status="active").count()
    disabled_author_count = Author.objects.filter(status="disabled").count()
    comment_count = Comment.objects.all().count()
    latest_post = Post.objects.all().order_by('-publish')[:3]
    latest_author = Author.objects.all().order_by('-date_joined')[:3]
    latest_comment = Comment.objects.all().order_by('-created')[:3]
    activity = LogEntry.objects.filter(
        Q(content_type__model="author")|
        Q(content_type__model="post")|
        Q(content_type__model="comment")|
        Q(content_type__model="role")|
        Q(content_type__model="Categories")
    ).order_by('-action_time')[:5]
    
    
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
    
    
    context = {
        "post_count":post_count,
        "author_count":author_count,
        "disabled_author_count":disabled_author_count,
        "comment_count":comment_count,
        "activity":activity,
        "latest_post":latest_post,
        "latest_author":latest_author,
        "latest_comment":latest_comment,
        "sd":sd
    }
    return render(request,'dashboard/home.html', context)