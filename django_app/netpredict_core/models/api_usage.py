from django.db import models
from django.utils import timezone

class ApiUsage(models.Model):
    """
    Tracks NetPredict usage per user per day.
    """
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    date = models.DateField(default=timezone.now)

    total_requests = models.IntegerField(default=0)
    exact_score_requests = models.IntegerField(default=0)

    class Meta:
        unique_together = ("user", "date")