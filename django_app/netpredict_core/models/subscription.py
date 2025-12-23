import uuid
from django.db import models
from django.contrib.auth.models import User

class SubscriptionPlan(models.Model):
    """
    Defines NetPredict Django Model: SubscriptionPlan
    Payment-agnostic (Stripe, Paypal, M-pesa, etc.) subscription plans.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)

    daily_request_limit = models.IntegerField()
    api_access = models.BooleanField(default=False)
    premium_features = models.BooleanField(default=False)

    allow_exact_score= models.BooleanField(default=False)
    allow_odds_calibration = models.BooleanField(default=False)
    allow_historical_data = models.BooleanField(default=False)
    allow_global_leagues = models.BooleanField(default=False)
    price_per_month = models.DecimalField(max_digits=8, decimal_places=2)


    def __str__(self):
        return self.name