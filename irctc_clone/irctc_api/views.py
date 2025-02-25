# from django.shortcuts import render
# from django.contrib.auth import get_user_model
# from django.contrib.auth.hashers import make_password
# from django.contrib.auth import authenticate
# from django.db import transaction
# from django.views import View
# from irctc_api.models import Train, Ticket
# from django.db import transaction
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.authtoken.models import Token
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response

# User = get_user_model()
# # Create your views here.


# class user_reg(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         # is_admin = request.data.get('is_admin', False)
#         email = request.data.get('email')

#         if User.objects.filter(username=username).exists():
#             return Response({"error": "User already exists"}, status=400)
    
#         user = User.objects.create_user(username=username, password=password, email=email)
#         # user.is_admin = is_admin
#         user.save()
        
#         return Response({"message": "User registered successfully!"})
    
# class user_login (APIView):
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(username=username, password=password)
#         if user:
#             return Response({"message": "User logged in successfully"}, status=200)
#             # token, created = Token.objects.get_or_create(user=user)
#             # return Response({"token": token.key})
#         return Response({"error": "Invalid credentials"}, status=400)

# class add_train (APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         if not(request.user.is_admin):
#             return Response({"message": "User must be admin to add train"})
        
#         t_name = request.data.get('t_name')
#         source = request.data.get('source')
#         destination = request.data.get('destination')
#         seats = request.data.get('seats')

#         train = Train.objects.create(name = t_name, source = source, destination = destination, total_seats = seats)
        
#         return Response({"message": f"Train Number {train.num} added successfully"})

# class check_availability (APIView):
#     permission_classes = [AllowAny]

#     def get(self, request, *args, **kwargs):
#         source = request.query_params.get('source')
#         destination = request.query_params.get('destination')

#         train = Train.objects.filter(source=source, destination=destination)

#         avlbl_seats = train.num_seats - Ticket.get_objects.count()
#         data = [{"train_number": train.train_num, "train_name": train.train_name, "source": train.source, "destination": train.destination, "available": avlbl_seats}]

#         return Response(data)

# class book_seat(APIView):
#     permission_classes = [IsAuthenticated]

#     @transaction.atomic
#     def post(self, request, *args, **kwargs):
#         train_num = request.data.get("train_number")
#         train = Train.objects.select_for_update().get(id = train_num)

#         booked_seats = Ticket.objects.filter(train=train).count()
#         if booked_seats < train.num_seats:
#             seat_number = booked_seats + 1
#             Ticket.objects.create(user=request.user, train=train, seat_num=seat_number)
#             return Response({"message": "Seat booked successfully!", "seat_number": seat_number})
#         else:
#             return Response({"error": "No seats available"}, status=400)

# class booking_details(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         bookings = Ticket.objects.filter(user=request.user)
#         data = [{"train": booking.train.name, "seat_number": booking.seat_num, "booked_at": booking.book_time} for booking in bookings]
#         return Response(data)


from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.db import transaction
from django.views import View
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from irctc_api.models import Train, Ticket
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
# from rest_framework.decorators import api_view, permission_classes

User = get_user_model()


class user_reg(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if User.objects.filter(username=username).exists():
            return Response({"error": "User already exists"}, status=400)

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        return Response({"message": "User registered successfully!"}, status=201)


class user_login(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"message": "User logged in successfully", "token": token.key}, status=200)

        return Response({"error": "Invalid credentials"}, status=400)

class add_train(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        
        api_key = request.headers.get("X-Admin-API-Key")
        if api_key != settings.ADMIN_API_KEY:
            return Response({"error": "Wrong API key"})
            raise PermissionDenied("Invalid API Key. Access Denied.")

        if not hasattr(request.user, 'is_admin') or not request.user.is_admin:
            return Response({"error": "User must be an admin to add a train"}, status=403)

        t_name = request.data.get('t_name')
        source = request.data.get('source')
        destination = request.data.get('destination')
        seats = request.data.get('seats')

        train = Train.objects.create(name=t_name, source=source, destination=destination, total_seats=seats)
        return Response({"message": f"Train {train.name} added successfully!", "train_id": train.id}, status=201)



class check_availability(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        source = request.query_params.get('source')
        destination = request.query_params.get('destination')

        if not source or not destination:
            return Response({"error": "Source and Destination required"}, status=400)

        trains = Train.objects.filter(source=source, destination=destination)
        data = []

        for train in trains:
            booked_seats = Ticket.objects.filter(train=train).count()
            available_seats = train.total_seats - booked_seats

            data.append({
                "train_number": train.id,
                "train_name": train.name,
                "source": train.source,
                "destination": train.destination,
                "available_seats": available_seats
            })

        return Response(data, status=200)


class book_seat(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        train_num = request.data.get("train_number")

        try:
            train = Train.objects.select_for_update().get(id=train_num)
        except Train.DoesNotExist:
            return Response({"error": "Train not found"}, status=404)

        booked_seats = Ticket.objects.filter(train=train).count()
        if booked_seats < train.total_seats:
            seat_number = booked_seats + 1
            Ticket.objects.create(user=request.user, train=train, seat_num=seat_number)
            return Response({"message": "Seat booked successfully!", "seat_number": seat_number}, status=201)

        return Response({"error": "No seats available"}, status=400)


class booking_details(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        bookings = Ticket.objects.filter(user=request.user)
        data = [{
            "train": booking.train.name,
            "seat_number": booking.seat_num,
            "booked_at": booking.book_time
        } for booking in bookings]

        return Response(data, status=200)
