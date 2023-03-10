from django.urls import path

from . import views

urlpatterns = [
    path("categories/", views.CategoryView.as_view()),
    path("categories/<uuid:pk>/", views.CategoryDetailView.as_view()),
    path("categories/reset/<uuid:pk>/", views.ResetCategoryView.as_view())
]
