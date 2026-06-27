from django.db import models


class StatusMusic(models.TextChoices):
    pending = 'PENDING', 'pending'
    processing = 'PROCESSING', 'processing'
    ready = 'READY', 'ready'
    failed = 'FAILED', 'failed'
