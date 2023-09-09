from django.db import models

# Create your models here.
class Text(models.Model):
  plaintext = models.CharField(max_length=255)