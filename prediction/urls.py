from .views import PredictionListView, PredictView
from django.urls import path

urlpatterns =[
    path('predict/',PredictView.as_view(), name='predict'),
    path('predictions/', PredictionListView.as_view(), name='prediction-list'),
]