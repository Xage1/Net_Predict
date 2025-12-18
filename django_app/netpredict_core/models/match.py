"""
NetPredict Django Model: Match
Stores match-level data for Poisson/ML simulations.
Includes home/away goals, xG, red cards, and league context.
"""

import uuid
from django.db import models
from .league import League
from .team import Team

class Match(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="matches")
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="home_matches")
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="away_matches")

    home_goals = models.PositiveSmallIntegerField(default=0)
    away_goals = models.PositiveSmallIntegerField(default=0)
    home_xg = models.FloatField(null=True, blank=True)
    away_xg = models.FloatField(null=True, blank=True)
    home_red_cards = models.PositiveSmallIntegerField(default=0)
    away_red_cards = models.PositiveSmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "netpredict_match"
        ordering = ["-date"]
        indexes = [
            models.Index(fields=['league', 'date']),
            models.Index(fields=['home_team', 'away_team']),
        ]
        constraints = [
            models.CheckConstraint(check=~models.Q(home_team=models.F('away_team')), name='home_neq_away')
        ]

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} ({self.date})"