from django.test import TestCase, Client
from django.urls import reverse
from .models import Appointment
from django.contrib.auth.models import User

class AppointmentTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password')
        
        # Login the user
        self.client = Client()
        self.client.login(username='testuser', password='password')

        # Test data
        self.appointment_data = {
            'name': 'John Doe',
            'appointment_date': '2024-12-05',
            'description': 'Annual check-up'
        }

    def test_add_appointment_view(self):
        # Call the add_appointment view with POST data
        response = self.client.post(reverse('add-appointment'), self.appointment_data)

        # Check if the response is a redirect (success case)
        self.assertEqual(response.status_code, 302)

        # Verify that the appointment is created in the database
        appointment = Appointment.objects.get(name='John Doe')
        self.assertEqual(appointment.description, 'Annual check-up')

    def test_add_appointment_template_rendering(self):
        # Test GET request for rendering the add appointment page
        response = self.client.get(reverse('add-appointment'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add-appointment.html')
