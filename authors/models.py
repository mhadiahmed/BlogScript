from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Author(AbstractUser):
    NOTIFICATION = (
        ('all','all posts'),
        ('none','do note send notification'),
        ('own posts','own posts'),
        )
    STATUS = (
        ('active','Active'),
        ('disabled','Disable'),
    )
    role = models.ForeignKey('Role',related_name='user_roles', on_delete=models.CASCADE, null=True)
    notification = models.CharField(max_length=20, choices=NOTIFICATION, default="none")
    status = models.CharField(max_length=20, choices=STATUS, default="disabled")

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
    

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def get_absolute_url(self):
        
        return reverse('authors', kwargs={'pk': self.pk})


class Role(models.Model):
    role_name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def __str__(self) -> str:
        return f"{self.role_name}"
