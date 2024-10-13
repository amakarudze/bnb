from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from . import views

app_name = "accounts"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html",
            extra_context={
                "title": "Login",
                "form": LoginForm(),
            },
        ),
        name="login",
    ),  # Using Django LoginView
    path("create_staff/", views.create_staff, name="create_staff"),
    path("signup/", views.signup, name="signup"),
]
