from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from users.forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'


class ProfileUpdate(UpdateView):
    model = get_user_model()
    fields = ('first_name', 'last_name', 'username')
    template_name = 'users/profile.html'

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, id=self.request.user.id)

    def get_success_url(self):
        username = get_object_or_404(self.model, id=self.request.user.id).username
        return reverse('profile', kwargs={'username': username})



