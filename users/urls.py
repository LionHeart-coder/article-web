from django.urls import path

from users.views import (ActivationDone, ProfileUpdate, SignUp,
                         check_user_token, create_done, resending_email)

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('update-profile/', ProfileUpdate.as_view(), name='update-profile'),
    path('create-done/<email>/<token>/', create_done, name='create-done'),
    path('check-user-token/', check_user_token, name='heck-user-token'),
    path('registration-done/', ActivationDone.as_view(), name='activate-done'),
    path('resending-email/<email>/<token>/', resending_email, name='resending-email'),
]
