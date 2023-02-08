from django.urls import path
from . import views

urlpatterns = [
    path('',views.stat_home, name='stats-home'),
]