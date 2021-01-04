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
    path("logout/",views.logout,name="logout"),
    path("subject1/",views.subject1,name="subject1"),
path("subject2/",views.subject2,name="subject2"),
path("subject3/",views.subject3,name="subject3"),
path("subject4/",views.subject4,name="subject4"),
path("subject5/",views.subject5,name="subject5"),
    path("result/",views.result,name="result"),
    path("analysis/",views.analysis,name="analysis"),
    path("report/",views.report,name="report")
]