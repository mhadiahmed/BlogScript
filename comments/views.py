from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse
from django.views.generic import ListView, DeleteView
from .models import Comment
from django.contrib import messages


class CommentListView(ListView):
    model = Comment
    template_name = "comments/comment_list.html"
    def get_queryset(self):
        qs = super(CommentListView, self).get_queryset()
        post_filter = self.request.GET.get('post_filter')
        if post_filter and post_filter != "all":
            qs = qs.filter(status=post_filter)
        return qs

class CommentDeleteView(DeleteView):
    model = Comment
    success_url = "/comments/"


def change_comment_status(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        comment_status = request.POST.get("comment")
        comment.status = comment_status
        comment.save()
        messages.success(request, f"Your comment {comment_status} successfully.")
        return redirect(reverse('comments:list'))