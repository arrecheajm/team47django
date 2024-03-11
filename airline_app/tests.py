'''
## [1.0.0] - 2024-02-24
### Added
- OnboardingTest.
- EmailTest.
- RegisterViewTestCase.
'''

from django_project.settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from django.core import mail
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class RegisterViewTestCase(TestCase):

    def test_register_view(self):
        # create a new user account
        response = self.client.post(reverse('register'),
            {
                'username': 'test_username',
                'password1': 'test_password',
                'password2': 'test_password',
                'email': 'test_username@utdallas.edu',
            })
        self.assertEqual(response.status_code, 200)

    def test_register_existing_username(self):
        # Create a user with the username 'existing_user'
        _ = User.objects.create_user(
            username='existing_user',
            password='password123',
            email='existing_user@utdallas.edu',
            )

        # Try to register with the same 'existing_user' username
        response = self.client.post(
            reverse('register'), {
                'username': 'existing_user',
                'password1': 'test_password',
                'password2': 'test_password',
                'email': 'existing_user@utdallas.edu',
            })

        # Assert that the response redirects to the registration_problem.html page
        self.assertEqual(response.status_code, 200)

class EmailTest(TestCase):

    def test_sending_email(self):
        subject = 'EmailTest'
        message = 'Test message.'
        from_email= f'Airline Admin <{DEFAULT_FROM_EMAIL}>'
        recipient_list = ['gjd190000@utdallas.edu']
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        # Assert that the email is sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'EmailTest')
        self.assertEqual(mail.outbox[0].from_email, f'Airline Admin <{DEFAULT_FROM_EMAIL}>')
        self.assertEqual(mail.outbox[0].to, ['gjd190000@utdallas.edu'])
        self.assertEqual(mail.outbox[0].body, 'Test message.')

class OnboardingTest(TestCase):
    def test_onboarding_template_display(self):
        response = self.client.get(reverse('onboarding'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'onboarding.html')
        self.assertContains(response, "Registration Successful")