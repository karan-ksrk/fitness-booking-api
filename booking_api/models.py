from django.db import models
from pytz import timezone


class FitnessClass(models.Model):
    name = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    available_slots = models.PositiveIntegerField()

    # Function to get the start time in a specific timezone
    def get_time_in_timezone(self, tz_str):
        return self.start_time.astimezone(timezone(tz_str))

    def __str__(self):
        return f"{self.name} by {self.instructor} on {self.start_time}"


class Booking(models.Model):
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client_name} - {self.fitness_class.name}"
