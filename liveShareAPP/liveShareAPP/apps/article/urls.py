from django.urls import path, re_path
from . import views


urlpatterns = [
    path("image/", views.ImageAPIView.as_view()), #　文章图片上传模块
    path("collection/", views.CollectionAPIView.as_view()), # 创建　展示文集
    re_path("article_info/(?P<pk>\d+)/", views.ArticleInfoAPIView.as_view()),
    re_path("collection/(?P<pk>\d+)/", views.CollectionDetailAPIView.as_view() ), #　编辑文集
    path("delete_collection/", views.DeleteCollection.as_view()), #　删除文集
    path("delete_article/", views.DeleteArticle.as_view()), #删除文章
    path("special/", views.SpecialCreatAPIView.as_view()), # 增加专题
    re_path("special/list/", views.SpecialListAPIView.as_view()), #专题模块展示
    path("post/special/", views.ArticlePostSpecialAPIView.as_view()),


]


from rest_framework.routers import SimpleRouter
router = SimpleRouter()
router.register("", views.ArticleAPIView) #　文章
urlpatterns += router.urls