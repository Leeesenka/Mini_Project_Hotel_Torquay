from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, DeleteView, UpdateView
from hotel.models import Booking, Room, User, Review
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from hotel.forms import BookingForm
from datetime import datetime
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import UserPassesTestMixin
# Create your views here.

class ListBookings(UserPassesTestMixin, ListView):
    template_name = "staff/list_bookings.html"
    model = Booking
    context_object_name = 'bookings'
    ordering = ['check_in_date']
   
    def test_func(self):
        return self.request.user.is_staff

    
class BookingView(UserPassesTestMixin, SuccessMessageMixin, DetailView, DeleteView):
    template_name = 'staff/detail_booking.html'
    context_object_name = 'info'
    model = Booking
    success_url = reverse_lazy('list_bookings')
    success_message = "The booking was deleted"
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(BookingView, self).delete(request, *args, **kwargs)
    def test_func(self):
        return self.request.user.is_staff 

class BookingUpdateView(UserPassesTestMixin, UpdateView):
    template_name = 'staff/edit_booking.html'
    model = Booking
    form_class = BookingForm
    success_url = reverse_lazy('list_bookings')
    def test_func(self):
        return self.request.user.is_staff
    

@staff_member_required(login_url='login')
def search_availability(request):
    check_in_date = request.GET.get('check_in_date')
    check_out_date = request.GET.get('check_out_date')

    if check_in_date is None or check_out_date is None:
        error_message = "Please enter check-in and check-out dates."
        return render(request, 'staff/staff_create_booking.html', {'error_message': error_message})

    check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date()
    check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d').date()

    if check_out_date <= check_in_date:
        error_message = "Check-out date must be after check-in date."
        return render(request, 'staff/staff_create_booking.html', {'error_message': error_message})

    request.session['check_in_date'] = check_in_date.isoformat()
    request.session['check_out_date'] = check_out_date.isoformat()

    return redirect('staff_room_selection')

@staff_member_required(login_url='login')
def room_selection(request):
    check_in_date = request.session.get('check_in_date')
    check_out_date = request.session.get('check_out_date')

    booked_rooms = Booking.objects.filter(
        check_in_date__lt=check_out_date,
        check_out_date__gt=check_in_date
    ).values_list('room', flat=True)

    available_rooms = Room.objects.exclude(id__in=booked_rooms)

    return render(request, 'staff/staff_available_rooms.html', {'available_rooms': available_rooms, 'check_in_date': check_in_date, 'check_out_date': check_out_date})

def calculate_total_price(check_in_date, check_out_date, price_per_night):
    check_in = datetime.strptime(check_in_date, '%Y-%m-%d')
    check_out = datetime.strptime(check_out_date, '%Y-%m-%d')
    days = (check_out - check_in).days

    total_price = days * price_per_night
    return total_price
    
@staff_member_required(login_url='login')   
def staff_room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    check_in_date = request.session.get('check_in_date')
    check_out_date = request.session.get('check_out_date')
    users = User.objects.all()
    total_price = calculate_total_price(check_in_date, check_out_date, room.price_per_night)

    return render(request, 'staff/staff_finish_booking.html', {'users': users, 'room': room, 'check_in_date': check_in_date, 'check_out_date': check_out_date, 'total_price': total_price})

@staff_member_required(login_url='login')    
def staff_book_room(request, room_id):
    if request.method == 'POST':
        check_in_date = request.session.get('check_in_date')
        check_out_date = request.session.get('check_out_date')

        if check_in_date is None or check_out_date is None:
            messages.error(request, 'Please select check-in and check-out dates before booking a room.')
            return redirect('staff_create_booking')

        room = get_object_or_404(Room, id=room_id)
        
        user = User.objects.get(id=request.POST.get('user')) 
        total_price = calculate_total_price(check_in_date, check_out_date, room.price_per_night)
        number_of_guests = request.POST.get('number_of_guests')

        if number_of_guests is None:
            messages.error(request, 'Please enter the number of guests before booking a room.')
            return redirect('staff_create_booking')

        booking = Booking(total_price=total_price, room=room, user=user, check_in_date=check_in_date, check_out_date=check_out_date, number_of_guests=number_of_guests)
        booking.save()

        messages.success(request, 'Your room has been successfully booked!')
        return redirect('list_bookings')
    else:
        return redirect('staff_room_booking', room_id=room_id)
    
class ReviewsView(UserPassesTestMixin ,ListView):
    template_name = "staff/list_reviews.html"
    model = Review
    context_object_name = 'reviews'
    ordering = ['created_at']
   
    def test_func(self):
        return self.request.user.is_staff
    
class ReviewDetail(UserPassesTestMixin, SuccessMessageMixin, DeleteView, DetailView):
    template_name = 'staff/detail_review.html'
    context_object_name = 'info'
    model = Review
    success_url = reverse_lazy('list_reviews')
    success_message = "The review was deleted"
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ReviewDetail, self).delete(request, *args, **kwargs)
    def test_func(self):
        return self.request.user.is_staff 