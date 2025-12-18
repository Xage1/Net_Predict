"""
NetPredict Django Model: Odds
Stores betting odds for ML calibration and probabilistic outputs.
"""

import uuid
from django.db import models
from .match import Match

class Odds(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.OneToOneField(Match, on_delete=models.CASCADE, related_name="odds")

    home_win = models.FloatField(null=True, blank=True)
    draw = models.FloatField(null=True, blank=True)
    away_win = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "netpredict_odds"

    def __str__(self):
        return f"Odds for {self.match}"
