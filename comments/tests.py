from authors.models import Author, Role
from django.test import TestCase
from django.urls import reverse
from model_bakery import baker
from posts.models import Post
from .models import Comment


class TestCommentView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.role = Role.objects.create(role_name="admin")
        cls.author = Author.objects.create(
            first_name="mahdi",
            last_name="ahmed",
            username="mahdiahmed",
            email="mahdi@email.com",
            password="newpassword",
            role=cls.role,
            status="active"
        )
        cls.category = baker.make('posts.Categories')
        cls.siteSettings = baker.make('site_settings.SiteSetting')
        cls.siteSettings = baker.make('site_settings.option')
        cls.post = Post.objects.create(author=cls.author, category=cls.category, title="new title" , body="test text", status="draft")
        cls.comment = Comment.objects.create(post=cls.post,name="mahdi", email="mahdi@mahdi.com", body="test", status="approved")
        # self.comment = baker.make('comments.Comment')
        
    def test_view_url_exists_at_desaired_location(self):
        response = self.client.get('/comments/')
        self.assertEqual(response.status_code, 200)
    
    def test_views_url_accessible_by_name(self):
        response = self.client.get(reverse('comments:list'))
        self.assertEqual(response.status_code, 200)
    
    def test_views_uses_correct_template(self):
        response = self.client.get(reverse('comments:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comments/comment_list.html')
    
    def test_views_context_has_all_comments(self):
        response = self.client.get(reverse('comments:list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.comment, response.context['comment_list'])