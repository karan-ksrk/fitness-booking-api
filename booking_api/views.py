from django.shortcuts import render
from .models import FitnessClass, Booking
from rest_framework.views import APIView
from django.utils import timezone
from .serializers import FitnessClassListSerializer, CreateBookingSerializer, BookingListSerializer
from rest_framework.response import Response 
from rest_framework import serializers, status


class FitnessClassListView(APIView):
    def get(self, request):
        tz_str = request.query_params.get('tz', 'Asia/Kolkata')
        classes = FitnessClass.objects.filter(start_time__gte=timezone.now()).order_by('start_time')

        data = []
        for cls in classes:
            serialized = FitnessClassListSerializer(cls).data
            serialized['start_time'] = cls.get_time_in_timezone(tz_str).isoformat()
            data.append(serialized)

        return Response(data)


class BookingCreateView(APIView):
    def post(self, request):
        class_id = request.data.get('class_id')
        client_name = request.data.get('client_name')
        client_email = request.data.get('client_email')

        # Check if all required fields are present
        if not all([class_id, client_name, client_email]):
            return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CreateBookingSerializer(data=request.data)

        if serializer.is_valid():
            try:
                booking = serializer.save()
                return Response({
                    "message": "Booking created successfully",
                    "booking": serializer.data
                }, status=status.HTTP_201_CREATED)
            except serializers.ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingListView(APIView):
    def get(self, request):
        client_email = request.query_params.get('email')
        if not client_email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BookingListSerializer(Booking.objects.filter(client_email=client_email), many=True)
        result = serializer.data
        return Response(result)
