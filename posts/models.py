from posts.utils import unique_slug_generator
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver
from authors.models import Author
from ckeditor.fields import RichTextField
from django.urls import reverse
# Create your models here.


class Post(models.Model):
    """Model definition for Post."""
    
    STATUS = (('active','Active'),
            ('Draft', 'Draft'))
    author = models.ForeignKey(Author, related_name="author_posts", on_delete=models.CASCADE)
    category = models.ForeignKey('Categories', related_name="post_category", on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255)
    # body = models.TextField()
    body = RichTextField()
    slug = models.SlugField(null=True, blank=True)
    image = models.ImageField(upload_to="uploads/", blank=True, null=True)
    meta_tag_title = models.CharField("Meta Title",max_length=255, blank=True, null=True)
    meta_tag_description = models.TextField("Meta Description",blank=True, null=True)
    meta_tag_keywords = models.TextField("Meta Keywords",blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default="Draft")
    publish = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)
    featured = models.BooleanField(default=False)
    
    class Meta:
        """Meta definition for Post."""

        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
    
    def get_absolute_url(self):
        return reverse('core:detail', kwargs={'slug': self.slug})

    def __str__(self):
        """Unicode representation of Post."""
        return f"{self.title}"


    
    @property
    def sd(self):
        return{
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": self.title,
            "image": "",  
            "author": {
                "@type": "BlogPosting",
                "name": self.author.first_name
            },  
            "publisher": {
                "@type": "Organization",
                "name": "NETBLOG",
                "logo": {
                "@type": "ImageObject",
                "url": self.get_absolute_url()
                }
            },
            "datePublished": self.publish
            }

@receiver(pre_save, sender=Post)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        
        
class Categories(models.Model):
    """Model definition for Categories."""
    
    STATUS = (('active','Active'),
            ('Draft', 'Draft'))
    
    
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default="active")
    # meta_title = models.CharField("Meta title", max_length=255)
    # meta_keywords = models.JSONField("Meta keywords")
    # meta_description = models.TextField("Meta description")
    class Meta:
        """Meta definition for Categories."""

        verbose_name = 'Categories'
        verbose_name_plural = 'Categories'
    
    def get_absolute_url(self):
        return reverse('core:category', kwargs={'pk': self.pk})

    def __str__(self):
        """Unicode representation of Categories."""
        return f"{self.name}"
