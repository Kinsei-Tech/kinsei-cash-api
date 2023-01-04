from django.urls import path
from .views import ExcelAutoView
urlpatterns = [
    path('excel/', ExcelAutoView.as_view()),
]
