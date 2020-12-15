from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from . import views
from django.contrib.auth import views as v
urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/",views.login,name="Login"),
    path("change/",views.change_password,name="Change"),
    path("",views.Dashboard,name="Dashboard"),
    path("logout/",views.logout,name="logout")
]