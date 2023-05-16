from django.urls import path
from .views import ListBookings, BookingView, BookingUpdateView, search_availability, room_selection, staff_room_detail, staff_book_room, ReviewsView, ReviewDetail

urlpatterns = [
    path('bookings/', ListBookings.as_view() , name='list_bookings'),
    path('bookings/<int:pk>/', BookingView.as_view() , name='detail_booking'),
    path('bookings/<int:pk>/edit/', BookingUpdateView.as_view() , name='edit_booking'),
    path('bookings/create/', search_availability , name='staff_create_booking'),
    path('bookings/create/selectroom/', room_selection , name='staff_room_selection'),
    path('bookings/create/selectroom/<int:room_id>/', staff_room_detail , name='staff_room_booking'),
    path('bookings/create/selectroom/<int:room_id>/finish/', staff_book_room , name='staff_room_booking_finish'),
    path('reviews/', ReviewsView.as_view(), name='list_reviews'),
    path('reviews/<int:pk>/', ReviewDetail.as_view(), name='detail_review'),    
]