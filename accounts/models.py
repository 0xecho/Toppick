from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class CustomUser(AbstractUser):
    telegram_id = models.CharField(max_length=255, blank=True, null=True)
    telegram_username = models.CharField(max_length=255, blank=True, null=True)
    is_public = models.BooleanField(default=True)
    public_url_uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return self.telegram_username or self.username