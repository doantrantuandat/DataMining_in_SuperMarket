from django.urls import path
from . import views
urlpatterns = [
    path('', views.algorithm, name='mining-home'),
    path('rule/', views.calculate, name='rules'),
]