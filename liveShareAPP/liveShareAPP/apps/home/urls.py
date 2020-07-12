from django.urls import path,re_path
from . import views
urlpatterns = [
    path("article/", views.ArticleListAPIView.as_view() ),
]

