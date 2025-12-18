"""
NetPredict Django Model: PlayerMatchStats
Tracks individual player statistics per match.
Supports future ML features and deep learning embeddings.
"""

import uuid
from django.db import models
from .player import Player
from .match import Match

class PlayerMatchStats(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="player_stats")
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="match_stats")

    minutes_played = models.PositiveSmallIntegerField(default=0)
    xg = models.FloatField(default=0.0)
    xa = models.FloatField(default=0.0)

    class Meta:
        db_table = "netpredict_player_match_stats"
        unique_together = ("match", "player")
        indexes = [
            models.Index(fields=['player', 'match']),
        ]

    def __str__(self):
        return f"{self.player} stats for {self.match}"