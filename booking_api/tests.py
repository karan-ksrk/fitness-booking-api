from rest_framework.test import APITestCase
from .models import FitnessClass, Booking
from datetime import datetime
from django.utils.timezone import make_aware
from django.urls import reverse


class BookingTestCase(APITestCase):
    def setUp(self):
        self.time1 = make_aware(datetime(2025, 6, 15, 8, 0))
        self.time2 = make_aware(datetime(2025, 6, 15, 10, 0))
        self.time3 = make_aware(datetime(2025, 6, 16, 7, 0))
        self.class1 = FitnessClass.objects.create(name="Yoga", instructor="Alice", start_time=make_aware(
            datetime(2025, 6, 15, 8, 0)), available_slots=5)
        self.class2 = FitnessClass.objects.create(name="Zumba", instructor="Bob", start_time=make_aware(
            datetime(2025, 6, 15, 10, 0)), available_slots=8)
        self.class3 = FitnessClass.objects.create(name="HIIT", instructor="Charlie", start_time=make_aware(
            datetime(2025, 6, 16, 7, 0)), available_slots=6)

    def test_get_classes(self):
        url = reverse('classes')
        # Test that we can get a list of classes
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['name'], 'Yoga')
        self.assertEqual(response.data[1]['name'], 'Zumba')
        self.assertEqual(response.data[2]['name'], 'HIIT')

        # Test that we can get a list of classes in a specific timezone
        url = reverse('classes') + '?tz=UTC'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['name'], 'Yoga')
        self.assertEqual(response.data[1]['name'], 'Zumba')
        self.assertEqual(response.data[2]['name'], 'HIIT')

        # check that the time is converted to the specified timezone
        converted_time1 = self.class1.get_time_in_timezone('UTC').isoformat()
        converted_time2 = self.class2.get_time_in_timezone('UTC').isoformat()
        converted_time3 = self.class3.get_time_in_timezone('UTC').isoformat()
        self.assertEqual(response.data[0]['start_time'], converted_time1)
        self.assertEqual(response.data[1]['start_time'], converted_time2)
        self.assertEqual(response.data[2]['start_time'], converted_time3)

    # Test that booking is successful

    def test_booking_success(self):
        url = reverse('book')
        data = {'class_id': self.class1.id, 'client_name': 'John Doe',
                'client_email': 'jDw0B@example.com'}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], 'Booking created successfully')
        self.class1.refresh_from_db()
        self.assertEqual(self.class1.available_slots, 4)

    # Test that booking fails when missing fields
    def test_booking_failure_missing_fields(self):
        url = reverse('book')
        data = {'client_name': 'John Doe',
                'client_email': 'jDw0B@example.com'}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'Missing fields')

    # Test that booking fails when there is an existing booking
    def test_booking_failure_existing_booking(self):
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

    # Test that booking fails when there are no available slots
    def test_booking_failure_no_available_slots(self):
        url = reverse('book')
        self.class1.available_slots = 0
        self.class1.save()
        data = {'class_id': self.class1.id, 'client_name': 'John Doe',
                'client_email': 'jDw0B@example.com'}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)
        self.assertIn('No available slots for this class', str(response.data['error']))

    # Test that booking fails when class is not found
    def test_booking_failure_class_not_found(self):
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
