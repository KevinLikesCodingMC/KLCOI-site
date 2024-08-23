from django.contrib import admin
from django.urls import path
from django.urls import re_path
from django.conf import settings
from django.views import static
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', views.index),
    path('view/<int:blog_id>/', views.blog_view),
    path('upload/add/', views.upload_add),
    path('upload/update/', views.upload_update),
]
