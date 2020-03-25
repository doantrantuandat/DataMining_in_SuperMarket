from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.algorithm, name='mining-home'),
    path('rule/', views.calculate, name='rules'),
    path('rulefordatabase/', views.calculate_database, name='rulesfromdatabase')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
