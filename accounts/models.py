from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Reservation(models.Model):
    guest_name = models.CharField(max_length=100)
    room_number = models.CharField(max_length=10)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    reservation_type = models.CharField(max_length=50, default="reservation")  # or walk-in

    def __str__(self):
        return f"{self.guest_name} - {self.room_number}"
