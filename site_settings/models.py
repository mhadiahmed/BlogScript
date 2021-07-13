from django.db import models
from authors.models import Author
# Create your models here.

class SiteSetting(models.Model):
    """Model definition for SiteSetting."""
    author = models.ForeignKey(Author,related_name="sitesettings", on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField("Site Name", max_length=255)
    description = models.TextField("Description")
    url = models.URLField("Site URL")
    # meta_title = models.CharField("Meta title", max_length=255)
    # meta_keywords = models.JSONField("Meta keywords")
    # meta_description = models.TextField("Meta description")
    
    class Meta:
        """Meta definition for SiteSetting."""

        verbose_name = 'SiteSetting'
        verbose_name_plural = 'SiteSettings'

    def __str__(self):
        """Unicode representation of SiteSetting."""
        return f"{self.name}"


class Option(models.Model):
    """Model definition for Option."""
    author = models.ForeignKey(Author,related_name="option", on_delete=models.SET_NULL, null=True, blank=True)
    POST_ORDER = (('new on top', 'NEW on top'),
                    ('new at the bottom', 'NEW at the bottom'))
    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
    number_of_posts_per_page = models.DecimalField("Number of posts per page",decimal_places=0, max_digits=100)
    posts_order = models.CharField('Post order', max_length=50, choices=POST_ORDER)
    allow_comment_posting = models.BooleanField("Allow comments posting",choices=BOOL_CHOICES,default=True)
    comment_approval = models.BooleanField("Comments Approval",choices=BOOL_CHOICES,default=True)
    comment_order = models.CharField('Comment order', max_length=50, choices=POST_ORDER)
    show_categories = models.BooleanField(choices=BOOL_CHOICES, default=True)

    class Meta:
        """Meta definition for Option."""

        verbose_name = 'Option'
        verbose_name_plural = 'Options'

    # def __str__(self):
    #     """Unicode representation of Option."""
    #     pass


# class Protection(models.Model):
#     """Model definition for Protection."""
#     pass

#     class Meta:
#         """Meta definition for Protection."""

#         verbose_name = 'Protection'
#         verbose_name_plural = 'Protections'

#     def __str__(self):
#         """Unicode representation of Protection."""
#         pass
