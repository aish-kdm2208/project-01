from django.db import models

# Create your models here.
class items(models.Model):
    id=models.AutoField(primary_key=True)
    item=models.CharField(max_length=20)
    status=models.CharField(max_length=20)
