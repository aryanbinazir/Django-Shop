from django.urls import path, include
from . import views

app_name = 'accounts'

password_url = [
    path('', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('confirm/<uidb64>/<token>', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('complete/', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete')
]

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('verify/register/', views.UserRegisterVerifyCodeView.as_view(), name='user_register_verify_code'),

    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('verify/login/', views.UserLoginVerifyCodeView.as_view(), name='user_login_verify_code'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('password/reset/', include(password_url))

]