from django.urls import path
from .views import IndexView, CADSystemListView, CADSystemDetailView, ContactsView, AboutView

app_name = 'myapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('cad_systems/', CADSystemListView.as_view(), name='cad_systems'),
    path('cad_systems/<slug:slug>/', CADSystemDetailView.as_view(), name='cad_detail'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('about/', AboutView.as_view(), name='about'),
    path('articles/', ArticleListView.as_view(), name='articles'),
    path('articles/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
]