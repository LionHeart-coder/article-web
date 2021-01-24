from posts.models import Comment, Post
from posts.tests.test_settings import TestSettings


class PostModelTest(TestSettings):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.post = Post.objects.create(
            text='Тестовый тест, который должен работать и будет работать',
            author=cls.user,
            group=cls.group,
        )

    def test_verbose_name(self):
        field_verboses = {
            'text': 'Текст',
            'group': 'Группа',
            'image': 'Картинка',
        }
        self.check_model_fields(self.post, field_verboses, 'verbose_name')

    def test_help_text(self):
        field_help_text = {
            'text': 'Не пишите слишком длинные посты :)',
            'group': 'Группа к которой привязывается пост',
            'image': 'Картинка к посту',
        }
        self.check_model_fields(self.post, field_help_text, 'help_text')

    def test_method_str(self):
        post_text = 'Тестовый тест, который должен работать и будет работать'
        self.assertEqual(self.post.__str__(), post_text[:15])


class GroupModelTest(TestSettings):
    def test_verbose_name(self):
        field_verboses = {
            'title': 'Заголовок',
            'slug': 'Слаг',
            'description': 'Описание',
        }
        self.check_model_fields(self.group, field_verboses, 'verbose_name')

    def test_help_text(self):
        field_help_text = {
            'title': 'Название группы',
            'slug': 'Адрес для страницы с группой (только латиница)',
            'description': 'Описание группы',
        }
        self.check_model_fields(self.group, field_help_text, 'help_text')

    def test_method_str(self):
        title = self.group.title
        self.assertEqual(title, 'test')


class TestCommentModel(TestSettings):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.post = Post.objects.create(
            text='Post for comment', group=cls.group, author=cls.user,
        )
        cls.comment = Comment.objects.create(
            post=cls.post, author=cls.user, text='comment text',
        )

    def test_verbose_name(self):
        field_verboses = {
            'text': 'Текст комментария',
            'created': 'Дата публикации',
        }
        self.check_model_fields(self.comment, field_verboses, 'verbose_name')

    def test_help_text(self):
        self.assertEqual(
            self.comment._meta.get_field('text').help_text,
            'Здесь вы можете написать своё мнение по поводу поста',
        )
