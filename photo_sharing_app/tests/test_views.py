from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from ..models import Post

class IndexViewWithPostsTestCase(TestCase):
    def setUp(self):
        self.posted_by = User.objects.create_user(
            username='testuser',
            password='testpasswd'
        )

        self.post1 = Post.objects.create(
            posted_by=self.posted_by,
            title='タイトル1',
            content='本文1'
        )
        self.post1.created_at = timezone.now()
        self.post1.save()

        self.post2 = Post.objects.create(
            posted_by=self.posted_by,
            title='タイトル2',
            content='本文2'
        )
        self.post2.created_at = timezone.now() + timedelta(days=1)
        self.post2.save()

    def test_index_returns_200(self):
        response = self.client.get(reverse('photo_sharing_app:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_uses_index_template(self):
        response = self.client.get(reverse('photo_sharing_app:index'))
        self.assertTemplateUsed(response, 'photo_sharing_app/index.html')

    def test_index_lists_posts_newest_first(self):
        response = self.client.get(reverse('photo_sharing_app:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context['posts'],
            [self.post2, self.post1]
        )
        self.assertContains(response, 'タイトル1')
        self.assertContains(response, 'タイトル2')

class IndexViewWithoutPostsTestCase(TestCase):
    def test_index_displays_empty_message_when_no_posts(self):
        response = self.client.get(reverse('photo_sharing_app:index'))
        self.assertContains(response, 'まだ投稿がありません。')
