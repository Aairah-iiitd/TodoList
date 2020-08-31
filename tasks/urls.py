from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name = "create"),
    path("completed", views.viewcompleted, name = "viewcompleted"),
    path("priority/<int:p_id>", views.viewpriority, name = "viewpriority"),
    path("done/<int:t_id>", views.markdone, name = "done"),
    path("change/<int:t_id>", views.changepriority, name = "change"),

]
