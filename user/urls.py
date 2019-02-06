from django.urls import path
from .views import login_for_modal, login, register, user_info, logout, change_nickname, bind_email, send_varification_code, change_password, forgot_password


urlpatterns = [
    path('login_for_modal/', login_for_modal, name='login_for_modal'),
    path('login/', login, name='login'),
    path('regsiter/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('user_info/', user_info, name='user_info'),
    path('change_nickname/', change_nickname, name='change_nickname'),
    path('bind_email/', bind_email, name='bind_email'),
    path('send_varification_code/', send_varification_code, name='send_varification_code'),
    path('change_password/', change_password, name='change_password'),
    path('forgot_password/', forgot_password, name='forgot_password'),

]
