from django.contrib.sites.models import Site
from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch.dispatcher import receiver
from authors.models import Author
from ckeditor.fields import RichTextField
from .utils import create_flat_page_template, delete_flat_page_template
from django.db import models
from django.urls import NoReverseMatch, get_script_prefix, reverse
from django.utils.encoding import iri_to_uri
from django.utils.translation import gettext_lazy as _
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


class Page(models.Model):
    STATUS = (('active','Active'),
            ('Draft', 'Draft'))
    url = models.CharField(_('URL'), max_length=100, db_index=True)
    title = models.CharField(_('title'), max_length=200)
    content = RichTextField()
    status = models.CharField(max_length=20, choices=STATUS, default="active")
    template_name = models.CharField(
        _('template name'),
        max_length=70,
        blank=True,
        help_text=_(
            'Example: “flatpages/contact_page.html”. If this isn’t provided, '
            'the system will use “flatpages/default.html”.'
        ),
    )
    
    registration_required = models.BooleanField(
        _('registration required'),
        help_text=_("If this is checked, only logged-in users will be able to view the page."),
        default=False,
    )
    sites = models.ManyToManyField(Site, verbose_name=_('sites'))
    class Meta:
        db_table = 'django_pages'
        verbose_name = _('pages')
        verbose_name_plural = _('pages')
        ordering = ['url']

    def __str__(self):
        return "%s -- %s" % (self.url, self.title)

    def get_absolute_url(self):
        from .views import page

        for url in (self.url.lstrip('/'), self.url):
            try:
                return reverse(page, kwargs={'url': url})
            except NoReverseMatch:
                pass
        # Handle script prefix manually because we bypass reverse()
        return iri_to_uri(get_script_prefix().rstrip('/') + self.url)    
    

@receiver(pre_save, sender=Page)
def post_save_receiver(sender, instance, *args, **kwargs):
    if not instance.template_name:
        instance.template_name = create_flat_page_template(instance.title)
        
@receiver(pre_delete, sender=Page)
def post_save_receiver(sender, instance, *args, **kwargs):
    delete_flat_page_template(instance.title)