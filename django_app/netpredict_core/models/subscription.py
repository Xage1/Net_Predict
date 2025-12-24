import uuid
from django.db import models
from django.contrib.auth.models import User

class SubscriptionPlan(models.Model):
    """
    NetPredict Subscription Plan

    - Payment-provider agnostic (Stripe, PayPal, M-Pesa, Visa)
    - Defines limits, features, and pricing
    - Used for both Web and API access control
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Identity
    name = models.CharField(max_length=50, unique=True)

    # Request limits
    daily_request_limit = models.PositiveIntegerField()
    monthly_request_limit = models.PositiveIntegerField()

    # API access
    api_access = models.BooleanField(default=False)

    # Feature flags
    allow_exact_score = models.BooleanField(default=False)
    exact_score_monthly_limit = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Null means unlimited (Elite)"
    )

    allow_odds_calibration = models.BooleanField(default=False)
    allow_historical_data = models.BooleanField(default=False)
    allow_global_leagues = models.BooleanField(default=False)

    # Pricing
    price_per_month = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Monthly price in USD-equivalent"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (${self.price_per_month}/mo)"
