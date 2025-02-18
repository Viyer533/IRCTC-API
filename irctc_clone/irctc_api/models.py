from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    # u_name = models.CharField(max_length=100, default="Guest")
    # pwd = models.CharField(max_length=50, default="password123")
    ph_no = models.BigIntegerField(default=9999999999) 
    email = models.EmailField(max_length=50, default="user@example.com", unique = True)

    def __str__(self):
        return self.username

class Train(models.Model):
    train_num = models.AutoField(primary_key=True) 
    train_name = models.CharField(max_length=255, default="Train")
    source = models.CharField(max_length=255, default="Source")
    dest = models.CharField(max_length=255, default="Destination")
    num_seats = models.IntegerField(default=100)

    def __str__(self):
        return f"{self.name} ({self.num})"

class Ticket(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    source = models.CharField(max_length=255, default="Source")
    dest = models.CharField(max_length=255, default="Destination")
    seat_num = models.IntegerField(default=1)
    book_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Ticket {self.id} - {self.train.name} - Seat {self.seat_num}"
