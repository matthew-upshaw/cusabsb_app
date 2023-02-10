from django.urls import path
from . import views

urlpatterns = [
    path('<str:year>/',views.stat_home, name='stats-home'),
]