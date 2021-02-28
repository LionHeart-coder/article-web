from datetime import datetime

from django.contrib.auth import get_user_model, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, TemplateView

from users.forms import CreationForm, UserChangeForm
from users.utils import send_registration_mail

User = get_user_model()


class SignUp(CreateView):
    form_class = CreationForm
    template_name = 'users/signup.html'

    def get_success_url(self):
        email = self.object.email
        token = default_token_generator.make_token(self.object)
        return reverse('create-done', kwargs={'email': email, 'token': token})


class CreateDone(TemplateView):
    template_name = 'users/create_account_done.html'


class ActivationDone(TemplateView):
    template_name = 'users/activation_account_done.html'


class ProfileUpdate(UpdateView):
    form_class = UserChangeForm
    template_name = 'users/profile.html'

    def get_object(self, queryset=None):
        return get_object_or_404(User, id=self.request.user.id)

    def get_success_url(self):
        username = get_object_or_404(User, id=self.request.user.id).username
        return reverse('profile', kwargs={'username': username})


def create_done(request, email, token):
    if request.user.is_authenticated:
        return redirect('profile', username=request.user.username)
    user = get_object_or_404(User, email=email)
    if not default_token_generator.check_token(user, token):
        return HttpResponseBadRequest()
    time_to_resend = user.email_timestamp - int(datetime.now().timestamp())

    if time_to_resend <= 0:
        time_to_resend = 0
    context = {'email': user.email, 'time_to_resend': time_to_resend, 'token': token}
    return render(
        request,
        'users/create_account_done.html',
        context=context,
    )


# TODO переписать под View класс с методами get и post
def check_user_token(request):
    token = request.GET.get('token')
    email = request.GET.get('email')
    user = get_object_or_404(User, email=email)
    if token is None:
        return HttpResponseBadRequest()
    if user.is_active:
        return HttpResponseBadRequest()
    if not default_token_generator.check_token(user, token):
        return HttpResponseBadRequest()
    user.is_active = True
    user.save()
    login(request, user)
    return redirect('activate-done')


def resending_email(request, email, token):
    user = get_object_or_404(User, email=email)
    if user.is_active:
        return redirect('profile', username=user.username)
    if not default_token_generator.check_token(user, token):
        return JsonResponse({'status': 'error'})
    if user.email_timestamp - int(datetime.now().timestamp()) < 0:
        token = default_token_generator.make_token(user)
        send_registration_mail(user, token, email)
    return JsonResponse({'status': 'success'})


class CustomPasswordResetView(PasswordResetView):
    html_email_template_name = 'registration/html_password_reset_email.html'
