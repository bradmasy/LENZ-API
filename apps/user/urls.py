from django.urls import path
from .views import UsersView, UserLoginView, UserSignupView

urlpatterns = [
    path("users", UsersView.as_view(), name="users"),
    path("users/<int:pk>", UsersView.as_view(), name="users"),
    path("login", UserLoginView.as_view(), name="login"),
    path("signup", UserSignupView.as_view(), name="signup"),
]
