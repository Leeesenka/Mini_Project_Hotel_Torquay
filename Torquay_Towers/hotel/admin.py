from django.contrib import admin

# Register your models here.
from .models import  Room, Hotel, Booking, Review, InfoRequest, RoomImage


admin.site.register(Room)
admin.site.register(Hotel)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(InfoRequest)
admin.site.register(RoomImage)
