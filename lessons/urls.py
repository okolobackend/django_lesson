from django.urls import path

from lessons import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/v1/create_lesson', views.create_lesson_form, name='create_lesson_form'),
]
