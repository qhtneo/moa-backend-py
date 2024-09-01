from django.urls import path, include
from . import views

urlpatterns = [
    path('pybo/', views.index),
]
