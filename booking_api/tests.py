from rest_framework.test import APITestCase
from .models import FitnessClass, Booking
from datetime import datetime
from django.utils.timezone import make_aware
from django.urls import reverse
from django.test import override_settings
from pytz import timezone


def get_time_in_timezone(time, tz_str):

    return time.astimezone(timezone(tz_str)).strftime("%Y-%m-%d %H:%M:%S")


class BookingTestCase(APITestCase):
    TIME_ZONES = ['Asia/Kolkata', 'America/New_York', 'Europe/London', 'UTC']

    def setUp(self):
        """
        Set up test data
        """
        self.time1 = make_aware(datetime(2026, 6, 15, 8, 0))
        self.time2 = make_aware(datetime(2026, 6, 15, 10, 0))
        self.time3 = make_aware(datetime(2026, 6, 16, 7, 0))
        self.class1 = FitnessClass.objects.create(name="Yoga", instructor="Alice", start_time=make_aware(
            datetime(2026, 6, 15, 8, 0)), available_slots=5)
        self.class2 = FitnessClass.objects.create(name="Zumba", instructor="Bob", start_time=make_aware(
            datetime(2026, 6, 15, 10, 0)), available_slots=8)
        self.class3 = FitnessClass.objects.create(name="HIIT", instructor="Charlie", start_time=make_aware(
            datetime(2026, 6, 16, 7, 0)), available_slots=6)

    def test_get_classes(self):
        """
        Test that we can get a list of classes
        """
        url = reverse('classes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['name'], 'Yoga')
        self.assertEqual(response.data[1]['name'], 'Zumba')
        self.assertEqual(response.data[2]['name'], 'HIIT')

    def test_get_classes_with_timezone(self):
        """
        Test that we can get a list of classes in different timezones
        """
        for TIME_ZONE in self.TIME_ZONES:
            with override_settings(TIME_ZONE=TIME_ZONE):
                url = reverse('classes')
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                converted_time1 = get_time_in_timezone(self.class1.start_time, TIME_ZONE)
                converted_time2 = get_time_in_timezone(self.class2.start_time, TIME_ZONE)
                converted_time3 = get_time_in_timezone(self.class3.start_time, TIME_ZONE)
                self.assertEqual(response.data[0]['start_time'], converted_time1)
                self.assertEqual(response.data[1]['start_time'], converted_time2)
                self.assertEqual(response.data[2]['start_time'], converted_time3)

    def test_booking_success(self):
        """
        Test that we can book a class
        """
        url = reverse('book')
        data = {'class_id': self.class1.id, 'client_name': 'John Doe',
                'client_email': 'jDw0B@example.com'}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], 'Booking created successfully')
        self.class1.refresh_from_db()
        self.assertEqual(self.class1.available_slots, 4)

    def test_booking_failure_missing_fields(self):
        """
        Test that booking fails when required fields are missing
        """
        url = reverse('book')
        data = {'client_name': 'John Doe',
                'client_email': 'jDw0B@example.com'}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'Missing fields')

    def test_booking_failure_existing_booking(self):
        """
        Test that booking fails when a booking already exists
        """
        url = reverse('book')
        data = {'class_id': self.class1.id, 'client_name': 'John Doe',
                'client_email': 'jDw0B@example.com'}
        booking = Booking.objects.create(fitness_class=self.class1,
                                         client_name='John Doe', client_email='jDw0B@example.com')

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)
        self.assertIn(
            'Booking already exists for this class', response.data['error'],
        )

    def test_booking_failure_no_available_slots(self):
        """
        Test that booking fails when there are no available slots
        """
        url = reverse('book')
        self.class1.available_slots = 0
        self.class1.save()
        data = {'class_id': self.class1.id, 'client_name': 'John Doe',
                'client_email': 'jDw0B@example.com'}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)
        self.assertIn('No available slots for this class', str(response.data['error']))

    def test_booking_failure_class_not_found(self):
        """
        Test that booking fails when the class is not found
        """
        url = reverse('book')
        data = {'class_id': 999, 'client_name': 'John Doe',
                'client_email': 'jDw0B@example.com'}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('class_id', response.data)
        self.assertEqual(
            response.data['class_id'][0],
            'Invalid pk "999" - object does not exist.'
        )
