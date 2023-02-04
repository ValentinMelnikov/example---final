from django.urls import path

from django.contrib import admin

from webapp.views import ArticleCommentCreateView
from webapp.views.article_views import ArticleView, AddArticleView, DeleteArticle, ArticleUpdateView
from webapp.views.base import IndexRedirectView, IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/add', AddArticleView.as_view(), name='article_add'),
    path('article/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_update'),
    path('article/<int:pk>/delete/', DeleteArticle.as_view(), name='article_delete'),
    path('', IndexView.as_view(), name='index'),
    path('article/<int:pk>/', ArticleView.as_view(), name='article_view'),
    path('index/', IndexRedirectView.as_view(), name='article_index_redirect'),
    path('article/<int:pk>/comments/add/', ArticleCommentCreateView.as_view(), name='article_comment_add')
]
