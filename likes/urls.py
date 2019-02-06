from django.urls import path
from .views import like_change


urlpatterns = [
    path('like_change', like_change, name='like_change'),
]
