from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from prediction.utils import predict_stock

class Command(BaseCommand):
    help = 'Run LSTM prediction for one or all tickers'

    def add_arguments(self, parser):
        parser.add_argument('--ticker', type=str)
        parser.add_argument('--all', action='store_true')

    def handle(self, *args, **options):
        if not options['ticker'] and not options['all']:
            self.stderr.write("Provide --ticker or --all")
            return

        user = User.objects.first()  # default user
        tickers = []

        if options['all']:
           from prediction.models import Prediction
           tickers = Prediction.objects.values_list('ticker', flat=True).distinct()
        else:
            tickers = [options['ticker'].upper()]

        for ticker in tickers:
            try:
                result = predict_stock(ticker, user)
                self.stdout.write(
                    self.style.SUCCESS(f"{ticker}: ₹{result['next_day_price']:.2f} | prediction: {result['r2'] * 100:.2f}%")
                )
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"{ticker}: {str(e)}"))
