from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from .models import Comment, Post, SocialLink


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'preview_text', 'content', 'group', 'preview_image')
        widgets = {'content': CKEditorUploadingWidget()}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class SocialLinkForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = ('link_type', 'link')

    def is_unique(self, author):
        if SocialLink.objects.filter(user=author, link_type=self.cleaned_data['link_type']).exists():
            self.errors.update({'link_type': ['Данный тип ссылки уже присутствует на вашей странице.']})
            return False
        return True

