from django.urls import path
from irctc_api.views import user_reg, book_seat, check_availability, user_login, add_train, booking_details 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', user_reg.as_view(), name="register"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', user_reg.as_view(), name="register"),
    path('login/', user_login.as_view(), name="login"),
    path('add-train/', add_train.as_view(), name="add-train"),
    path('seat-availability/', check_availability.as_view(), name="seat-availability"),
    path('book-seat/', book_seat.as_view(), name="book-seat"), 
    path('booking-details/', booking_details.as_view(), name="booking-details")
]