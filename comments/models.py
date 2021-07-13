from django.db import models
from posts.models import Post


class Comment(models.Model):
    STATUS = (('approved', 'Approved'),
            ('pendding','Pendding'),
            ('not approved', 'Not approved'))
    post = models.ForeignKey(Post, related_name="post_comment", on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    status = models.CharField(max_length=30, choices=STATUS, default="pendding")
    
    class Meta:

        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
