from django.urls import path
from . import views
from transactions import views

urlpatterns = [
    path("transactions/", views.TransactionView.as_view()),
    path("transactions/<str:pk>/", views.TransactionDetailView.as_view()),
]
