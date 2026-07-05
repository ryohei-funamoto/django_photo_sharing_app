from datetime import timedelta
from urllib.parse import urlencode

from django.contrib.auth import get_user
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

class ShowViewTestCase(TestCase):
    def setUp(self):
        self.posted_by = User.objects.create_user(
            username='testuser',
            password='testpasswd'
        )

        self.post = Post.objects.create(
            posted_by=self.posted_by,
            title='タイトル',
            content='本文1\n本文2'
        )

    def test_show_returns_200(self):
        response = self.client.get(reverse('photo_sharing_app:show', kwargs={'id': self.post.id}))
        self.assertEqual(response.status_code, 200)

    def test_show_uses_detail_template(self):
        response = self.client.get(reverse('photo_sharing_app:show', kwargs={'id': self.post.id}))
        self.assertTemplateUsed(response, 'photo_sharing_app/detail.html')

    def test_show_returns_404_for_nonexistent_post(self):
        response = self.client.get(reverse('photo_sharing_app:show', kwargs={'id': self.post.id + 1}))
        self.assertEqual(response.status_code, 404)

    def test_show_displays_post_detail(self):
        response = self.client.get(reverse('photo_sharing_app:show', kwargs={'id': self.post.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post'], self.post)
        self.assertContains(response, 'タイトル')
        self.assertContains(response, '本文1<br>本文2', html=True)

class CreateViewTestCase(TestCase):
    def setUp(self):
        self.posted_by = User.objects.create_user(
            username='testuser',
            password='testpasswd'
        )
        self.create_url = reverse('photo_sharing_app:create')
        self.login_url = reverse('photo_sharing_app:login')
        self.redirect_url = f'{self.login_url}?{urlencode({"next": self.create_url})}'

    def test_create_redirects_to_login_when_anonymous_get(self):
        response = self.client.get(self.create_url)
        self.assertRedirects(response, self.redirect_url)

    def test_create_redirects_to_login_when_anonymous_post(self):
        response = self.client.post(self.create_url, {
            'title': 'タイトル',
            'content': '本文',
        })
        self.assertEqual(Post.objects.count(), 0)
        self.assertRedirects(response, self.redirect_url)

    def test_create_returns_200_when_authenticated(self):
        self.client.login(username='testuser', password='testpasswd')
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)

    def test_create_uses_create_template_when_authenticated(self):
        self.client.login(username='testuser', password='testpasswd')
        response = self.client.get(self.create_url)
        self.assertTemplateUsed(response, 'photo_sharing_app/create.html')

    def test_create_creates_post_when_authenticated(self):
        self.client.login(username='testuser', password='testpasswd')
        response = self.client.post(self.create_url, {
            'title': 'タイトル',
            'content': '本文',
        })
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.posted_by, self.posted_by)
        self.assertEqual(post.title, 'タイトル')
        self.assertEqual(post.content, '本文')
        self.assertRedirects(response, reverse('photo_sharing_app:index'))

    def test_create_renders_form_with_errors_when_input_is_empty(self):
        self.client.login(username='testuser', password='testpasswd')
        response = self.client.post(self.create_url, {
            'title': '',
            'content': '',
        })
        self.assertEqual(Post.objects.count(), 0)
        self.assertContains(response, 'タイトルを入力してください。')
        self.assertContains(response, '本文を入力してください。')

class LoginViewTestCase(TestCase):
    def setUp(self):
        self.posted_by = User.objects.create_user(
            username='testuser',
            password='testpasswd'
        )
        self.login_url = reverse('photo_sharing_app:login')
        self.index_url = reverse('photo_sharing_app:index')
        self.create_url = reverse('photo_sharing_app:create')

    def test_login_returns_200(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_login_uses_login_template(self):
        response = self.client.get(self.login_url)
        self.assertTemplateUsed(response, 'photo_sharing_app/registration/login.html')

    def test_login_logs_in_successfully_with_valid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpasswd',
        })
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.username, 'testuser')
        self.assertRedirects(response, self.index_url)

    def test_login_does_not_authenticate_with_wrong_password(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpasswd',
        })
        user = get_user(self.client)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertFalse(user.is_authenticated)

    def test_login_redirects_to_create_with_next_parameter(self):
        url_parameter = urlencode({'next': self.create_url})
        response = self.client.post(f'{self.login_url}?{url_parameter}', {
            'username': 'testuser',
            'password': 'testpasswd',
        })
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.username, 'testuser')
        self.assertRedirects(response, self.create_url)

    def test_login_redirects_authenticated_user_to_index(self):
        self.client.force_login(self.posted_by)
        response = self.client.get(self.login_url)
        self.assertRedirects(response, self.index_url)

class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.posted_by = User.objects.create_user(
            username='testuser',
            password='testpasswd'
        )

    def test_logout_redirects_to_login(self):
        self.client.login(username='testuser', password='testpasswd')
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.post(reverse('photo_sharing_app:logout'))
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)
        self.assertRedirects(response, reverse('photo_sharing_app:login'))
