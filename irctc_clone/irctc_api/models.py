from django.db import models

# Create your models here.
class User(models.Model):
    u_name = models.CharField(max_length=100)
    pwd = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)

class Train (models.Model):
    train_num = models.IntegerField()
    train_name = models.CharField(max_length = 100)
    source = models.CharField(max_length = 50)
    dest = models.CharField(max_length = 50)