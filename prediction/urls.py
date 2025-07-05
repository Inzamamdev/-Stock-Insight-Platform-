from .views import PredictionListView, PredictView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
urlpatterns =[
    path('predict/',PredictView.as_view(), name='predict'),
    path('predictions/', PredictionListView.as_view(), name='prediction-list'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)