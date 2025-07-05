from .utils import predict_stock
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.templatetags.static import static
import os
from .serializers import PredictRequestSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .models import Prediction
from .serializers import PredictionSerializer

class PredictView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PredictRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        ticker = serializer.validated_data['ticker']

        try:
            result = predict_stock(ticker, request.user)
            return Response({
                "next_day_price": result["next_day_price"],
                "mse": result["mse"],
                "rmse": result["rmse"],
                "r2": result["r2"],
                "plot_urls": [
                 result["plot_urls"][0],
                 result["plot_urls"][1]
                ]
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        



class PredictionListView(ListAPIView):
    serializer_class = PredictionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Prediction.objects.filter(user=self.request.user)

        ticker = self.request.query_params.get('ticker')
        if ticker:
            queryset = queryset.filter(ticker__iexact=ticker)

        date = self.request.query_params.get('date')
        if date:
            queryset = queryset.filter(created_at__date=date)

        return queryset.order_by('-created_at')