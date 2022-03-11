from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts.views import register_request, login_request,  logout_request, password_reset_request


urlpatterns = [
    path('register', register_request, name="register"),
    path('login', login_request, name="login"),
    path('logout', logout_request, name= "logout"),
    path("password_reset", password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),

]
