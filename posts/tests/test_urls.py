from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.urls import reverse

from posts.models import Post
from posts.tests.test_settings import TestSettings


class PostURLTests(TestSettings):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.post = Post.objects.create(
            text='Test URL', author=cls.user, group=cls.group
        )
        site = Site.objects.first()
        flatpages = {
            '/about-author/': ('about me', '<b>some content</b>'),
            '/about-spec/': ('about my tech', '<b>some content</b>'),
        }
        for url, body in flatpages.items():
            title, content = body
            flatpage = FlatPage.objects.create(
                url=url, title=title, content=content,
            )
            flatpage.sites.add(site)

    def check_status_code(self, patterns_with_codes, usertype):
        for pattern, code in patterns_with_codes.items():
            with self.subTest(pattern=pattern):
                response = usertype.get(pattern)
                self.assertEqual(response.status_code, code)

    def check_redirect(self, patterns_with_redirects, usertype):
        for pattern, redirect in patterns_with_redirects.items():
            with self.subTest(pattern=pattern, redirect_pattern=redirect):
                response = usertype.get(pattern)
                self.assertRedirects(response, redirect)

    def test_urls_authorized_client(self):
        patterns_and_codes = {
            reverse('index'): 200,
            reverse('group', kwargs={'slug': self.group.slug}): 200,
            reverse('new_post'): 200,
            reverse('profile', kwargs={'username': self.user.username}): 200,
            reverse('about_author'): 200,
            reverse('about_spec'): 200,
            reverse(
                'post',
                kwargs={
                    'username': self.user.username,
                    'post_id': self.post.id,
                },
            ): 200,
            reverse(
                'post_edit',
                kwargs={
                    'username': self.user.username,
                    'post_id': self.post.id,
                },
            ): 200,
            reverse('profile', kwargs={'username': 'DoesNotExist'}): 404,
            reverse('follow_index'): 200,
        }
        should_be_redirect_patterns = {
            reverse(
                'add_comment',
                kwargs={
                    'username': self.user.username,
                    'post_id': self.post.id,
                },
            ): reverse(
                'post',
                kwargs={
                    'username': self.user.username,
                    'post_id': self.post.id,
                },
            ),
            reverse(
                'profile_follow',
                kwargs={'username': self.user_not_author.username},
            ): reverse(
                'profile', kwargs={'username': self.user_not_author.username}
            ),
            reverse(
                'profile_unfollow',
                kwargs={'username': self.user_not_author.username},
            ): reverse(
                'profile', kwargs={'username': self.user_not_author.username}
            ),
        }
        self.check_status_code(patterns_and_codes, self.authorized_client)
        self.check_redirect(
            should_be_redirect_patterns, self.authorized_client
        )

    def test_urls_anonymous_client(self):
        patterns_and_codes = {
            reverse('index'): 200,
            reverse('group', kwargs={'slug': self.group.slug}): 200,
            reverse('profile', kwargs={'username': self.user.username}): 200,
            reverse('about_author'): 200,
            reverse('about_spec'): 200,
            reverse(
                'post',
                kwargs={
                    'username': self.user.username,
                    'post_id': self.post.id,
                },
            ): 200,
        }

        redirect_url = reverse('login') + '?next='
        should_be_redirect_patterns = {
            reverse('new_post'): redirect_url + reverse('new_post'),
            reverse('follow_index'): redirect_url + reverse('follow_index'),
            reverse(
                'add_comment',
                kwargs={
                    'username': self.user.username,
                    'post_id': self.post.id,
                },
            ): redirect_url
            + reverse(
                'add_comment',
                kwargs={
                    'username': self.user.username,
                    'post_id': self.post.id,
                },
            ),
            reverse(
                'profile_follow',
                kwargs={'username': self.user_not_author.username},
            ): redirect_url
            + reverse(
                'profile_follow',
                kwargs={'username': self.user_not_author.username},
            ),
            reverse(
                'profile_unfollow',
                kwargs={'username': self.user_not_author.username},
            ): redirect_url
            + reverse(
                'profile_unfollow',
                kwargs={'username': self.user_not_author.username},
            ),
        }
        self.check_status_code(patterns_and_codes, self.client)
        self.check_redirect(should_be_redirect_patterns, self.client)

    def test_edit_post_url_authorized_client_not_author(self):
        pattern = reverse(
            'post_edit',
            kwargs={'username': self.user.username, 'post_id': self.post.id},
        )
        response = self.not_author.get(pattern)
        self.assertRedirects(
            response,
            reverse(
                'post',
                kwargs={
                    'username': self.user.username,
                    'post_id': self.post.id,
                },
            ),
        )

    def test_edit_post_url_anonymous_client(self):
        pattern = reverse(
            'post_edit',
            kwargs={'username': self.user.username, 'post_id': self.post.id},
        )
        redirect_url = reverse('login') + '?next=' + pattern
        response = self.client.get(pattern)
        self.assertRedirects(response, redirect_url)
