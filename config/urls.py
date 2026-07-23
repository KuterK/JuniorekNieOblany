from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from analyses.views import RegisterView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/register/", RegisterView.as_view(), name="register"),
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", include("analyses.urls")),
]
