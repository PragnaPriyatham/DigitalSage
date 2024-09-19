from django.db import models


class login(models.Model):
  userid = models.CharField(max_length=255)
  password = models.CharField(max_length=255)