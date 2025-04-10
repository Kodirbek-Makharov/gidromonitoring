from django.urls import path
from . import api_views as av

urlpatterns = [
    # path("api/dalolatnoma-list", views.index, name="index"),
    path('dalolatnoma-list', av.ApiDalolatnomaList.as_view()),
    path('dalolatnoma-list/<int:pk>', av.ApiDalolatnomaShow.as_view()),

]
