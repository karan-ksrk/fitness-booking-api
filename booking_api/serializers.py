from rest_framework import serializers
from .models import FitnessClass, Booking
from django.db import transaction
from django.utils.timezone import localtime


class FitnessClassListSerializer(serializers.ModelSerializer):
    start_time = serializers.SerializerMethodField()

    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'instructor', 'start_time', 'available_slots']

    def get_start_time(self, obj):
        return localtime(obj.start_time).strftime("%Y-%m-%d %H:%M:%S")


class BookingListSerializer(serializers.ModelSerializer):
    fitness_class = FitnessClassListSerializer()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ['id', 'fitness_class', 'client_name', 'client_email', 'created_at']

    def get_created_at(self, obj):
        return localtime(obj.created_at).strftime("%Y-%m-%d %H:%M:%S")


class CreateBookingSerializer(serializers.ModelSerializer):
    class_id = serializers.PrimaryKeyRelatedField(
        queryset=FitnessClass.objects.all(),
        source='fitness_class',
        write_only=True,
    )

    class Meta:
        model = Booking
        fields = ['class_id', 'client_name', 'client_email']

    def validate(self, data):
        """
        validate slot availability and duplicate bookings
        """

        fitness_class = data['fitness_class']
        client_email = data['client_email']

        if fitness_class.available_slots <= 0:
            raise serializers.ValidationError({"error": "No available slots for this class"})

        if Booking.objects.filter(fitness_class=fitness_class, client_email=client_email).exists():
            raise serializers.ValidationError({"error": "Booking already exists for this class"})

        return data

    def create(self, validated_data):
        """
        create new booking and decrement available slots
        """
        with transaction.atomic():
            fitness_class = FitnessClass.objects.select_for_update().get(
                id=validated_data['fitness_class'].id)  # select for update means lock the row for update

            # Double-check slots are still availabe (race condition protection)
            if fitness_class.available_slots <= 0:
                raise serializers.ValidationError("No available slots for this class")

            # Create the booking
            booking = super().create(validated_data)

            # Decrement available slots
            fitness_class.available_slots -= 1
            fitness_class.save()
        return booking

    def to_representation(self, instance):
        """
        Customize the output representation
        """
        representation = super().to_representation(instance)
        representation['booking_id'] = instance.id
        representation['fitness_class_name'] = instance.fitness_class.name
        representation['fitness_class_instructor'] = instance.fitness_class.instructor
        representation['fitness_start_time'] = instance.fitness_class.start_time if hasattr(
            instance.fitness_class, 'date') else None

        # Replace fitness_class ID with more detailed info
        representation['fitness_class'] = {
            'id': instance.fitness_class.id,
            'name': instance.fitness_class.name,
            'available_slots': instance.fitness_class.available_slots
        }

        return representation
