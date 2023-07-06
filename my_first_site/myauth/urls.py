from django.contrib.auth.views import LoginView
from django.urls import path

from .views import (
    login_view,
    set_cookie_view,
    get_cookie_view,
    set_session_view,
    get_session_view,
    logout_view,
    MyLogoutView,
    AboutMeView,
    RegisterView,
    FooBarView,
    UserUpdateView,
    UsersListView,
    ProfileDetailsView,
    HelloView,
)

app_name = "myauth"
urlpatterns = [
    # path("login/", login_view, name="login"),
    path("login/", LoginView.as_view(template_name="myauth/login.html", redirect_authenticated_user=True), name="login"),
    path('hello/', HelloView.as_view(), name='hello'),
    # path("logout/", logout_view, name="logout"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("about-me/", AboutMeView.as_view(), name="about-me"),
    path("users/", UsersListView.as_view(), name="users-list"),
    path("users/<int:pk>/", ProfileDetailsView.as_view(), name="user-profile"),
    path("register/", RegisterView.as_view(), name="register"),
    path("cookie/set/", set_cookie_view, name="cookie-set"),
    path("cookie/get/", get_cookie_view, name="cookie-get"),
    path("session/set/", set_session_view, name="session-set"),
    path("session/get/", get_session_view, name="session-get"),
    path("foo-bar/", FooBarView.as_view(), name="foo-bar"),
    path("about-me/<int:pk>/update/", UserUpdateView.as_view(), name="user-update")

]