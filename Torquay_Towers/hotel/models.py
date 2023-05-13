from django.db import models
from django.contrib.auth.models import User
# Create your models here.




class Room(models.Model):
    ROOM_TYPE_CHOICES = (
        ('single', 'Single Room'),
        ('double', 'Double Room'),
        ('deluxe', 'Deluxe'),
    )
    ROOM_TYPE_BEDS = (
        ('queen', 'Queen'),
        ('king', 'King'),
        ('twin', 'Twin'),
        ('hollywood twin', 'Hollywood twin'),
        ('double-double', 'Double-double'),
        ('Studio','Studio'),
    )
    ROOM_TYPE_SIZE = (
        ('smal', '20 m²'),
        ('medium', '30 m²'),
        ('big', '50 m²'),

    )
    
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES)
    capacity = models.PositiveIntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    room_number = models.PositiveIntegerField(unique=True, default=1)
    chalet_size = models.CharField(max_length=20, choices=ROOM_TYPE_SIZE, default=1)
    beds = models.CharField(max_length=50, choices=ROOM_TYPE_BEDS, default=1) 


    def __str__(self):
        return self.room_type


class Hotel(models.Model):
    name_hotel =  models.CharField()
    discription_hotel = models.CharField()
    location_hotel = models.CharField()
    environment_hotel = models.CharField()

    def __str__(self):
        return self.name_hotel



class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_guests = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.room.room_number} - {self.room.room_type} - {self.check_in_date} - {self.check_out_date}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.room.room_type} - {self.rating}"

class InfoRequest(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.email}"
    

class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='room_images/')

    def __str__(self):
        return f"Image for Room {self.room.room_number}"