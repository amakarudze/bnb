from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import LoginForm


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
]
