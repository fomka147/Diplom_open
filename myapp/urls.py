from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('cad_systems/', views.CADSystemListView.as_view(), name='cad_systems'),
    path('cad_systems/<int:pk>/', views.CADSystemDetailView.as_view(), name='cad_detail'),
    path('contacts/', views.contacts, name='contacts'),
    path('about/', views.about, name='about'),
]