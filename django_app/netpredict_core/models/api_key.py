import uuid
import secrets
from django.db import models
from django.contrib.auth.models import User


class APIKey(models.Model):
    """
    API Key for accessing NetPredict API.

    - Linked to a user
    - Used for authentication and rate limiting
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    key = models.CharField(max_length=64, unique=True, editable=False)
    name = models.CharField(max_length=100)  # e.g. "My Bot", "Mobile App"

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = secrets.token_hex(32)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.name}"