"""
NetPredict Django Model: Player
Encodes player identity, team, and position.
"""

import uuid
from django.db import models
from .team import Team

class Player(models.Model):
    POSITION_CHOICES = [
        ("GK", "Goalkeeper"),
        ("DEF", "Defender"),
        ("MID", "Midfielder"),
        ("FWD", "Forward"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="players")
    position = models.CharField(max_length=3, choices=POSITION_CHOICES)

    class Meta:
        db_table = "netpredict_player"
        unique_together = ("name", "team")
        indexes = [
            models.Index(fields=['team', 'position']),
        ]

    def __str__(self):
        return f"{self.name} ({self.position})"