from django.shortcuts import render, redirect
from datetime import date
from datetime import datetime
from .models import Room, Booking, Hotel, Review
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .forms import DateForm, ReviewForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):
    today = date.today().isoformat()
    return render(request, 'index.html', {'today': today})

def search_availability(request):
    check_in_date = request.GET.get('check_in_date')
    check_out_date = request.GET.get('check_out_date')

    if check_in_date is None or check_out_date is None:
        error_message = "Please enter check-in and check-out dates."
        return render(request, 'index.html', {'error_message': error_message})

    check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date()
    check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d').date()

    if check_out_date <= check_in_date:
        error_message = "Check-out date must be after check-in date."
        return render(request, 'index.html', {'error_message': error_message})

    request.session['check_in_date'] = check_in_date.isoformat()
    request.session['check_out_date'] = check_out_date.isoformat()

    return redirect('room_selection')

def room_selection(request):
    check_in_date = request.session.get('check_in_date')
    check_out_date = request.session.get('check_out_date')

    booked_rooms = Booking.objects.filter(
        check_in_date__lt=check_out_date,
        check_out_date__gt=check_in_date
    ).values_list('room', flat=True)

    available_rooms = Room.objects.exclude(id__in=booked_rooms)

    return render(request, 'available_rooms.html', {'available_rooms': available_rooms, 'check_in_date': check_in_date, 'check_out_date': check_out_date})

def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    check_in_date = request.session.get('check_in_date')
    check_out_date = request.session.get('check_out_date')

    total_price = calculate_total_price(check_in_date, check_out_date, room.price_per_night)

    return render(request, 'room_detail.html', {'room': room, 'check_in_date': check_in_date, 'check_out_date': check_out_date, 'total_price': total_price})

def calculate_total_price(check_in_date, check_out_date, price_per_night):
    check_in = datetime.strptime(check_in_date, '%Y-%m-%d')
    check_out = datetime.strptime(check_out_date, '%Y-%m-%d')
    days = (check_out - check_in).days

    total_price = days * price_per_night
    return total_price



def book_room(request, room_id):
    if request.method == 'POST':
        check_in_date = request.session.get('check_in_date')
        check_out_date = request.session.get('check_out_date')

        if not check_in_date or not check_out_date:
            messages.error(request, 'Please select check-in and check-out dates before booking a room.')
            return redirect('index')

        room = get_object_or_404(Room, id=room_id)
        user = request.user  # Assuming the user is logged in

        number_of_guests = int(request.POST.get('number_of_guests'))

        if number_of_guests is None:
            messages.error(request, 'Please enter the number of guests before booking a room.')
            return redirect('index')

        total_price = calculate_total_price(check_in_date, check_out_date, room.price_per_night)

        booking = Booking(room=room, user=user, check_in_date=check_in_date, check_out_date=check_out_date, number_of_guests=number_of_guests, total_price=total_price)
        booking.save()

        messages.success(request, 'Your room has been successfully booked!')
        return redirect('index')
    else:
        return redirect('room_detail', room_id=room_id)

    

def hotel_info(request):
    hotel = Hotel.objects.first()
    context = {'hotel': hotel}
    return render(request, 'index.html', context)    



@login_required
def submit_review(request):
    user = request.user

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            booking_id = request.POST.get('booking_id')
            booking = get_object_or_404(Booking, id=booking_id, user=user) 

            
            review = form.save(commit=False)
            review.user = user
            review.room = booking.room
            review.save()

            return HttpResponseRedirect(reverse('booking_details'))  
    else:
       
        bookings = Booking.objects.filter(user=user)

        
        if bookings.exists():
            form = ReviewForm()
            context = {'form': form, 'bookings': bookings}
            return render(request, 'review_form.html', context)
        else:
          
            error_message = "You don't have any bookings available to review."
            return render(request, 'error.html', {'error_message': error_message})

    context = {'form': form}
    return render(request, 'review_form.html', context)


@login_required
def booking_details(request):
    user_bookings = Booking.objects.filter(user=request.user)
    context = {'user_bookings': user_bookings}
    return render(request, 'booking_details.html', context)