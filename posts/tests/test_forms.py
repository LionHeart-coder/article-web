from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from posts.models import Comment, Group, Post
from posts.tests.test_settings import TestSettings


class PostCreateFormTest(TestSettings):
    def setUp(self):
        super().setUp()
        self.post = Post.objects.create(
            text='Test for form', author=self.user, group=self.group
        )

    def test_create_new_post_authorized_client(self):
        group = Group.objects.get(title='test')
        form_data = {'text': 'record text', 'group': group.id}

        response = self.authorized_client.post(
            reverse('new_post'), data=form_data, follow=True
        )
        post = Post.objects.first()
        self.assertEqual(response.status_code, 200)
        self.check_equivalence_objects(
            post, self.post, ('author', 'group'), text=form_data['text']
        )

    def test_create_new_post_anonymous_client(self):
        group = Group.objects.get(title='test')
        form_data = {'text': 'record text', 'group': group.id}
        response = self.client.post(reverse('new_post'), data=form_data,)
        post = Post.objects.first()
        self.check_equivalence_objects(
            post, self.post, ('text', 'author', 'group')
        )

    def test_edit_post_authorized_client_author(self):
        form_data = {'text': 'modified text', 'group': self.group.id}
        response = self.authorized_client.post(
            reverse(
                'post_edit',
                kwargs={
                    'username': self.user.username,
                    'post_id': self.post.id,
                },
            ),
            data=form_data,
            follow=True,
        )
        post = Post.objects.last()
        self.check_equivalence_objects(
            post, self.post, ('author', 'group'), text=form_data['text']
        )

    def test_edit_post_authorized_client_not_author(self):
        form_data = {'text': 'I am not author', 'group': self.group.id}
        response = self.not_author.post(
            reverse(
                'post_edit',
                kwargs={
                    'username': self.user.username,
                    'post_id': self.post.id,
                },
            ),
            data=form_data,
            follow=True,
        )
        post = Post.objects.last()
        self.check_equivalence_objects(
            post, self.post, ('text', 'group', 'author')
        )

    def test_edit_post_anonymous_client(self):
        form_data = {'text': 'I am anonymous', 'group': self.group.id}
        response = self.client.post(
            reverse(
                'post_edit',
                kwargs={
                    'username': self.user.username,
                    'post_id': self.post.id,
                },
            ),
            data=form_data,
            follow=True,
        )
        post = Post.objects.last()
        self.check_equivalence_objects(
            post, self.post, ('text', 'group', 'author')
        )

    def test_upload_graphic_file(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00'
            b'\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
            b'\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif', content=small_gif, content_type='image/gif'
        )
        form_data = {'text': 'test image', 'image': uploaded}
        response = self.authorized_client.post(
            reverse('new_post'), data=form_data, follow=True
        )
        post = Post.objects.first()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(post.image.__bool__())
        self.assertEqual(post.image.url, '/media/posts/small.gif')

    def test_upload_not_graphic_file(self):
        text = b'Some text'
        uploaded = SimpleUploadedFile(
            name='fake.jpg', content=text, content_type='image/jpg'
        )
        form_data = {'text': 'test image', 'image': uploaded}
        response = self.authorized_client.post(
            reverse('new_post'), data=form_data, follow=True
        )
        expected_error = (
            'Загрузите правильное изображение. Файл, '
            'который вы загрузили, поврежден или не является изображением.'
        )
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'image', expected_error)


class CommentCreateFormTest(TestSettings):
    def setUp(self):
        super().setUp()
        self.post = Post.objects.create(text='for comments', author=self.user,)

    def test_add_comment_anonymous_client(self):
        response = self.client.post(
            reverse(
                'add_comment',
                kwargs={'username': self.user, 'post_id': self.post.id},
            ),
            data={'text': 'test comments'},
            follow=True,
        )
        self.assertEqual(Comment.objects.count(), 0)

    def test_add_comment_authorized_client(self):
        field_value = {
            'text': 'test comments',
            'author': self.user,
            'post': self.post,
        }
        response = self.authorized_client.post(
            reverse(
                'add_comment',
                kwargs={'username': self.user, 'post_id': self.post.id},
            ),
            data={'text': field_value['text']},
            follow=True,
        )
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.last()
        self.check_statements_in_one_obj(comment, field_value)
