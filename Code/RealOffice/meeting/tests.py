from django.test import TestCase
from .models import *
# Create your tests here.

class MeetingTestClass(TestCase):
	def setUp(self):
		p = Person.objects.create(name="gen", email="s@s.com")

	def test_person_email(self):
		p1 = Person.objects.create(name="gen", email="s1@s.com")
		p2 = Person.objects.create(name="genu", email="s2@s.com")
		self.assertEqual(1+1, 2)
	def test_person_name(self):
		p1 = Person.objects.create(name="gen", email="s1@s.com")
		p2 = Person.objects.create(name="gen", email="s2@s.com")
		self.assertEqual(p2,!None)