from django.test import TestCase
from django.urls import reverse
from .models import Post
from django.contrib.auth.models import User

class NewsListTest(TestCase):

    def test_NewsListView_context(self):
        responce = self.client.get(reverse('news:post_list'))
        self.assertTrue('posts' in responce.context)

    def test_NewsListView_template(self):
        responce = self.client.get(reverse('news:post_list'))
        self.assertTemplateUsed(responce, "post_list.html")

    def test_NewsListView_responce(self):
        responce = self.client.get(reverse('news:post_list'))
        self.assertEqual(responce.status_code, 200)

class NewsDetailTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="Artur", password="1234qwer")
        self.post = Post.objects.create(title="Title", author=self.user, context="Text", draft=True)

    def test_NewsDetailView_context(self):
        responce = self.client.get(reverse('news:post_detail', kwargs={"slug": self.post.slug}))
        self.assertTrue('detail' in responce.context)
        self.assertTrue('comments' in responce.context)
        self.assertTrue('form' in responce.context)

    def test_NewsDetailView_template(self):
        pass

    def test_NewsDetailView_responce(self):
        pass