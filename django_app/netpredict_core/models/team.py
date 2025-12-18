"""
NetPredict Django Model: Team
Represents football teams linked to leagues.
"""

import uuid
from django.db import models
from .league import League

class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="teams")
    elo_rating = models.FloatField(default=1500.0)  # Standard Elo rating

    class Meta:
        db_table = "netpredict_team"
        ordering = ["league__tier", "name"]
        indexes = [
            models.Index(fields=['league', 'name']),
        ]

    def __str__(self):
        return self.name