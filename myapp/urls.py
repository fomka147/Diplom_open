from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('system/<slug:slug>/', views.system_detail, name='system_detail'),
    path('search/', views.search, name='search'),
]