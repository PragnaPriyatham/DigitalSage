from django.db import models


class login(models.Model):
  userid = models.CharField(max_length=255)
  password = models.CharField(max_length=255)

class laptops(models.Model):
    laptop_id = models.IntegerField(primary_key=True)
    Brand = models.CharField(max_length=100)
    class Meta:
        db_table = 'laptops'

    def __str__(self):
        return self.Brand

  