from django.urls import path

from . import views

app_name = "main"
urlpatterns = [
    path("", views.index, name="index"),
    path("scrape/", views.scrape, name="scrape"),
    path("add-webtoon/", views.addWebtoon, name="addWebtoon"),
    path("update-webtoon/<str:id>/", views.updateWebtoon, name="updateWebtoon"),
    path("delete-webtoon/<str:id>/", views.deleteWebtoon, name="deleteWebtoon"),
]
