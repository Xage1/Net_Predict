import uuid
from django.db import models

class League(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    tier = models.PositiveSmallIntegerField()
    goal_rate = models.FloatField(default=1.0)
    home_advantage = models.FloatField(default=1.0)
    variance_factor = models.FloatField(default=1.0)

    class Meta:
        db_table = 'leagues'
        ordering = ["tier", "name"]

    def __str__(self):
        return f"{self.name} ({self.country})"   