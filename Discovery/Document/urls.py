from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path 
from . import views

app_name = "Document"

urlpatterns = [
    path('', views.home, name='home'),
    path('schema/', views.schema, name='schema'),
    path('metrics/', views.metrics, name='metrics'),
    path('queries/', views.queries, name='queries'),
    path('update/', views.update, name='update'),
    path('upload/', views.upload, name='upload'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)