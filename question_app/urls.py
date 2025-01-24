from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generate-question/', views.generate_question, name='generate_question'),
]