from django import forms
from django.core.cache import cache
from django.urls import reverse

from posts import posts_settings
from posts.models import Comment, Follow, Post
from posts.tests.test_settings import TestSettings


class PaginatorTests(TestSettings):
    def setUp(self):
        super().setUp()
        for number in range(1, 14):
            Post.objects.create(
                text=f'Some text{number}', author=self.user, group=self.group
            )

    def check_statements_in_pagination(self, response, number_of_posts):
        posts_per_page = response.context['paginator'].per_page
        number_of_posts_on_page = (
            response.context['paginator'].page(1).object_list.count()
        )
        self.assertEqual(
            response.context['paginator'].count, Post.objects.count()
        )
        self.assertEqual(posts_per_page, number_of_posts)
        self.assertEqual(number_of_posts_on_page, number_of_posts)

    def test_pages_with_pagination(self):
        Follow.objects.create(user=self.user_not_author, author=self.user)
        patterns_and_number_of_posts = {
            reverse('index'): posts_settings.INDEX_NUMBER_OF_POSTS,
            reverse(
                'profile', kwargs={'username': self.user.username}
            ): posts_settings.PROFILE_NUMBER_OF_POSTS,
            reverse(
                'group', kwargs={'slug': self.group.slug}
            ): posts_settings.GROUP_NUMBER_OF_POSTS,
            reverse('follow_index'): posts_settings.FOLLOW_INDEX_NUMBER_OF_POSTS,
        }
        for pattern, number_per_page in patterns_and_number_of_posts.items():
            with self.subTest(pattern=pattern, number_of_page=number_per_page):
                response = self.not_author.get(pattern)
                self.check_statements_in_pagination(response, number_per_page)


class PostPagesTests(TestSettings):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.post = Post.objects.create(
            text='Test post pages group1', author=cls.user, group=cls.group
        )
        cls.comment = Comment.objects.create(
            post=cls.post, author=cls.user, text='comment text',
        )

    def get_post(self, response):
        cache.clear()
        self.assertEqual(
            response.context['paginator'].count, Post.objects.count()
        )
        post = response.context['page'][0]
        return post

    def test_pages_uses_correct_template(self):
        templates_page_names = {
            reverse('index'): 'posts/index.html',
            reverse('group', kwargs={'slug': self.group.slug}): 'group.html',
            reverse('new_post'): 'posts/new_post.html',
            reverse(
                'post_edit',
                kwargs={
                    'username': self.user.username,
                    'post_id': self.post.id,
                },
            ): 'posts/new_post.html',
        }
        for reverse_name, template in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def check_statements_in_context(self, context_obj, db_obj, fields: tuple):
        for field in fields:
            with self.subTest(
                    field=field, context_obj=context_obj, db_obj=db_obj
            ):
                self.assertEqual(
                    getattr(context_obj, field), getattr(db_obj, field),
                )

    def test_index_page_show_correct_context(self):
        response = self.authorized_client.get(reverse('index'))
        post = self.get_post(response)
        self.check_statements_in_context(
            post, self.post, ('text', 'author', 'group', 'comments')
        )

    def test_group_posts_show_correct_context(self):
        response = self.authorized_client.get(
            reverse('group', kwargs={'slug': self.group.slug})
        )
        post = self.get_post(response)
        group = response.context.get('group')
        self.check_statements_in_context(
            post, self.post, ('text', 'author', 'group', 'comments')
        )
        self.check_statements_in_context(
            group, self.group, ('title', 'slug', 'description')
        )

    def test_new_post_page_show_correct_context(self):
        response = self.authorized_client.get(reverse('new_post'))

        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_filed = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_filed, expected)

    def test_profile_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse('profile', kwargs={'username': self.user.username})
        )
        post = self.get_post(response)
        author = response.context.get('author')
        self.check_statements_in_context(
            post, self.post, ('text', 'author', 'group', 'comments')
        )
        self.check_statements_in_context(
            author, self.user, ('username', 'first_name', 'last_name')
        )

    def test_post_view_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse(
                'post',
                kwargs={
                    'username': self.user.username,
                    'post_id': self.post.id,
                },
            )
        )
        post = response.context.get('post')
        self.check_statements_in_context(
            post, self.post, ('text', 'author', 'group', 'comments')
        )

    def test_post_edit_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse(
                'post_edit',
                kwargs={
                    'username': self.user.username,
                    'post_id': self.post.id,
                },
            )
        )
        self.assertIn('form', response.context)
        self.assertIn('edit_post', response.context)

    def test_new_post_in_correct_group(self):
        response = self.client.get(
            reverse('group', kwargs={'slug': self.group.slug})
        )
        self.check_statements_in_context(
            self.post,
            self.get_post(response),
            ('text', 'group', 'author', 'comments'),
        )

    def test_new_post_not_in_incorrect_group(self):
        response = self.client.get(
            reverse('group', kwargs={'slug': self.group2.slug})
        )
        self.assertEqual(response.context['paginator'].count, 0)

    @staticmethod
    def profile_follow(user, author):
        user.get(
            reverse('profile_follow', kwargs={'username': author.username})
        )
        response = user.get(
            reverse('profile', kwargs={'username': author.username})
        )
        return response

    @staticmethod
    def profile_unfollow(user, author):
        user.get(
            reverse('profile_unfollow', kwargs={'username': author.username})
        )
        response = user.get(
            reverse('profile', kwargs={'username': author.username})
        )
        return response

    def test_follow_anonymous_client(self):
        response = self.profile_follow(self.client, self.user)
        self.assertEqual(Follow.objects.count(), 0)

    def test_follow_authorized_client(self):
        response = self.profile_follow(self.not_author, self.user)
        self.assertEqual(Follow.objects.count(), 1)
        self.check_statements_in_context(response.context['author'], self.user, ('following', 'follower'))

    def test_unfollowing_authorized_client(self):
        Follow.objects.create(user=self.user_not_author, author=self.user)
        response = self.profile_unfollow(self.not_author, self.user)
        self.assertEqual(Follow.objects.count(), 0)
        self.check_statements_in_context(response.context['author'], self.user, ('following', 'follower'))


class CacheTest(TestSettings):
    def setUp(self):
        super().setUp()
        cache.clear()

    def test_index_cache(self):
        response = self.client.get(reverse('index'))
        Post.objects.create(
            author=self.user,
            text='some text'
        )
        response_from_cache = self.client.get(reverse('index'))
        self.assertEqual(response.content, response_from_cache.content)
        cache.clear()
        response_without_cache = self.client.get(reverse('index'))
        self.assertNotEqual(
            response_from_cache.content, response_without_cache.content
        )
