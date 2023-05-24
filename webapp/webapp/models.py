from django.db import models
from django.contrib.auth.models import User


# class Dashboard(models.Model):
#     total_income = models.FloatField(default=0)
#     total_rooms = models.IntegerField(default=0)
#     total_reservations = models.IntegerField(default=0)
#     total_users = models.IntegerField(default=0)
#     images = image'leri priority'e göre al.

class Images(models.Model):
    id = models.Model.pk
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_created=True)
    image = models.ImageField()
    priority = models.IntegerField(default=0)


class Room(models.Model):
    id = models.Model.pk
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_created=True)
    name = models.CharField(max_length=255, default="")
    slug = models.CharField(max_length=255, default="")
    type = models.CharField(max_length=255, default="")
    location = models.CharField(max_length=255, default="")
    description = models.TextField()
    image_ids = models.ManyToManyField(Images, null=True)
    price = models.IntegerField()
    features = models.CharField(max_length=255, default="") #   arrayfield desteklemiyormuş, ',' ile ayırıp saklıyoruz. abi dJngo Çko iYYi
    is_active = models.BooleanField(default=True)
    reservation_id = models.ForeignKey('RoomReservation', on_delete=models.CASCADE, null=True)


class RoomReservation(models.Model):
    id = models.Model.pk
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_created=True)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    paid_amount = models.FloatField(default=0)
