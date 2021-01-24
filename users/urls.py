from django.urls import path

from users.views import SignUp, ProfileUpdate

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('update-profile/', ProfileUpdate.as_view(), name='update-profile')
]
