from django.core.management import BaseCommand
from ...models import FitnessClass, Booking
from datetime import datetime
from django.utils.timezone import make_aware


SAMPLE_CLASSES = {
    "Yoga": {
        "instructor": "Alice",
        "start_time": make_aware(datetime(2025, 6, 15, 8, 0)),
        "available_slots": 5
    },
    "Zumba": {
        "instructor": "Bob",
        "start_time": make_aware(datetime(2025, 6, 15, 10, 0)),
        "available_slots": 8
    },
    "HIIT": {
        "instructor": "Charlie",
        "start_time": make_aware(datetime(2025, 6, 16, 7, 0)),
        "available_slots": 6
    }
}


SAMPLE_BOOKINGs = {
    "Yoga": {
        "client_name": "John Doe",
        "client_email": "VXg9y@example.com"
    },
    "Zumba": {
        "client_name": "Jane Smith",
        "client_email": "VXg9y@example.com"
    }
}


class Command(BaseCommand):
    help = 'Add sample data to the database'

    def handle(self, *args, **kwargs):
        for name, data in SAMPLE_CLASSES.items():
            FitnessClass.objects.create(name=name, **data)

        for name, data in SAMPLE_BOOKINGs.items():
            fitness_class = FitnessClass.objects.get(name=name)
            Booking.objects.create(fitness_class=fitness_class, **data)

        self.stdout.write(self.style.SUCCESS('Sample data added successfully'))
