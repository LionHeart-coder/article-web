import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase

from posts.models import Group

User = get_user_model()

# не знаю насколько правильное решение, но так у нас одна папка и всё удаляется правильно
settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


class TestSettings(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            username='LionHeart', first_name='Sergey', last_name='Korsakov',
        )
        cls.group = Group.objects.create(
            title='test', slug='test-group', description='some description'
        )
        cls.group2 = Group.objects.create(
            title='test2', slug='test-group2', description='some description2'
        )
        cls.user_not_author = User.objects.create(username='NotAuthor')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        super().setUp()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.not_author = Client()
        self.not_author.force_login(self.user_not_author)
        cache.clear()

    def check_equivalence_objects(self, new_obj, db_obj, fields, **kwargs):
        for field in fields:
            with self.subTest(field=field, context_obj=new_obj, db_obj=db_obj):
                self.assertEqual(
                    getattr(new_obj, field), getattr(db_obj, field),
                )
        if kwargs:
            for extra_filed, value in kwargs.items():
                with self.subTest(
                    extra_filed=extra_filed,
                    value=value,
                    context_obj=new_obj,
                    db_obj=db_obj,
                ):
                    self.assertEqual(getattr(new_obj, extra_filed), value)

    def check_model_fields(self, model_obj, field_value, field_type):
        for value, expected in field_value.items():
            with self.subTest(value=value):
                self.assertEqual(
                    getattr(model_obj._meta.get_field(value), field_type),
                    expected,
                )

    def check_statements_in_one_obj(self, db_obj, field_value):
        for field, value in field_value.items():
            with self.subTest(field=field, value=value, db_obj=db_obj):
                self.assertEqual(getattr(db_obj, field), value)
