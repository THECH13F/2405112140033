from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class ShortUrls(models.Model):
    original = models.URLField()
    code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at