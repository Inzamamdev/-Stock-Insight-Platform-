from django.db import models
from django.contrib.auth.models import User

class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    next_day_price = models.FloatField()
    metrics = models.JSONField()
    plot_1_path = models.CharField(max_length=255)
    plot_2_path = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.ticker} - {self.created_at.strftime('%Y-%m-%d')}"
