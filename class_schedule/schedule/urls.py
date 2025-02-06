"""
URL configuration for class_schedule project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import list_classes, create_class, delete_class_view, editar_estudiantes
urlpatterns = [
    path("", list_classes, name="list_classes"),
    path("create/", create_class, name="create_class"),
    path("edit_students/", editar_estudiantes, name="edit_students"),
    path("delete/<int:row>/<int:col>/", delete_class_view, name="delete_class"),
]
