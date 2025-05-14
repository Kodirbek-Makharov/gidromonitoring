from django.urls import path
from . import api_views as av

urlpatterns = [
    # path("api/dalolatnoma-list", views.index, name="index"),
    path('dalolatnoma-list', av.ApiDalolatnomaList.as_view()),
    path('dalolatnoma-list/<int:pk>', av.ApiDalolatnomaShow.as_view()),
    path('get-user', av.api_get_user),
    path('get-viloyat', av.api_get_viloyat),
    path('get-tuman', av.api_get_tuman),
    path('get-nht', av.api_get_nht),
    path('get-stansiya', av.api_get_stansiya),
]
