from django.urls import path

from . import views

urlpatterns = [
    path("categories/", views.CategoryView.as_view()),
    path("categories/<uuid:pk>/", views.CategoryDetailView.as_view()),
    path("categories/healthy/", views.HealthyCategories.as_view()),
]
