from django.test import TestCase
from .models import Author, Role
from django.urls import reverse
from model_bakery import baker
# Create your tests here.

class TestAuthorViews(TestCase):
    def setUp(self):
        self.role = Role.objects.create(role_name="admin")
        self.siteSettings = baker.make("site_settings.SiteSetting")
        self.option = baker.make("site_settings.option")
        self.author = Author.objects.create(
            email="mahdiahmed@test.com",
            first_name="mahdi",
            last_name="ahmed",
            role=self.role)
        
    def test_author_list_view(self):
        res = self.client.get(reverse('authors:authors'))
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.author, res.context['author_list'])
    
    def test_author_edit_view(self):
        pass
    
    
    def test_author_create_view(self):
        pass
    
    def test_author_delete_view(self):
        pass