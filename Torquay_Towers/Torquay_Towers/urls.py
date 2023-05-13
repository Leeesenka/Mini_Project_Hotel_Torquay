
from django.contrib import admin
from django.urls import path
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls.static import static
from django.conf import settings
from accounts.views import (ProfileView,
                    SignUpView,
                    profile_redirect_view,
                    )
from hotel.views import index, room_detail, calculate_total_price, search_availability, room_selection, book_room

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile-redirect/', profile_redirect_view, name='profile-redirect'),
    path('index/', index, name='index'),
    path('search_availability/', search_availability, name='search_availability'),
    path('room/<int:room_id>/', room_detail, name='room_detail'),
    path('book_room/<int:room_id>/', book_room, name='book_room'),
    path('room_selection/', room_selection, name='room_selection'),
    # path('calculate_price/<int:room_id>/', calculate_price_view, name='calculate_price'),
    path('calculate_total_price/', calculate_total_price, name='calculate_total_price'),



]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

