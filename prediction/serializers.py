from rest_framework import serializers
from .models import Prediction

class PredictRequestSerializer(serializers.Serializer):
    ticker = serializers.CharField()



class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = ['id', 'ticker', 'next_day_price', 'metrics', 'created_at', 'plot_1_path', 'plot_2_path']