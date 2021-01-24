from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from ..models import Post
from .test_settings import TestSettings


class ImageTest(TestSettings):
    def test_image_tag_in_content(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00'
            b'\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
            b'\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile(
            name='small1.gif', content=small_gif, content_type='image/gif'
        )
        response = self.client.get(reverse('index'))
        number_of_img = response.content.decode('utf-8').count('<img')
        field_value = {
            'text': 'test text image',
            'image': uploaded,
        }
        Post.objects.create(
            author=self.user,
            text=field_value['text'],
            image=field_value['image'],
        )
        cache.clear()
        # TODO  проверка что картинок стала больше
        response = self.client.get(reverse('index'))
        self.assertEqual(Post.objects.count(), 1)
        self.assertContains(response, '<img', count=number_of_img + 1)
