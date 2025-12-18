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