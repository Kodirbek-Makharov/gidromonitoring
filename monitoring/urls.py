from django.urls import path, include
from . import views

urlpatterns = [
    path("api/", include("monitoring.api_urls")),
    path("", views.index, name="index"),
    # path("seed", views.seed, name="seed"),
    path("inspektorlar", views.user_list, name="user_list"),
    path("list", views.dalolatnoma_list, name="dalolatnoma_list"),
    path("<int:id>", views.dalolatnoma_one, name="dalolatnoma_one"),
    path("<int:id>/eliminated", views.dalolatnoma_bartaraf_etildi, name="bartaraf_etildi"),
    path("<int:id>/eliminated_admin", views.dalolatnoma_bartaraf_etildi_admin, name="bartaraf_etildi_admin"),
    # path("update/<int:id>", views.dalolatnoma_edit, name="dalolatnoma_edit"),
    path("new", views.dalolatnoma_new, name="dalolatnoma_new"),
    path("api/tuman", views.tuman_list, name="tuman_list"),
    path("api/xarita", views.xarita_from_to, name="xarita_from_to"),
    path("api/stansiya-seriya", views.stansiya_seriya, name="stansiya_seriya"),    
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("change-password", views.change_password, name="chp"),
]
