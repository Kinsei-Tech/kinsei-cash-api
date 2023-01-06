from django.urls import path
from . import views
from .views import ExcelAutoView
from transactions import views

urlpatterns = [
    path("transactions/", views.TransactionView.as_view()),
    path("transactions/<uuid:pk>/", views.TransactionDetailView.as_view()),
    path('excel/', ExcelAutoView.as_view()),
]
