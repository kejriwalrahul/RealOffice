# Django Imports
from django.test import TestCase, Client

# Rest Framework Imports
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

# Python Imports
from datetime import datetime, timedelta

# Project imports
from models import * 

class GenTestClass(TestCase):
	
	def setUp(self):
		user = User.objects.create_user('rahul', 'rahul@k.com', 'kejriwal')
		user.save()

		user_profile = UserProfile(user= user, is_admin=False)
		user_profile.save()

		# Get usr token
		response = Client().post('/login/', {'username':'rahul','password':'kejriwal'})
		token = response.data['token']

		# Create rest_client
		self.rest_client = APIClient()
		self.rest_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
	
		# Store Person
		p = Person(name='Suhaas', email='s@s.com')
		p.save()

		# Store Venues
		v = Venue(room='DCF', capacity=50, infrastructure='Computers, AC')
		v.save()
		v = Venue(room='CS25', capacity=100, infrastructure='AC')
		v.save()
		v = Venue(room='CS24', capacity=100, infrastructure='')
		v.save()

		# Store Workflow
		w = MeetingWorkflow(meetingType='Conference', actions='send reminders')
		w.save()

	def test_login_successful(self):
		c = Client()
		response = c.post('/login/', {'username':'rahul','password':'kejriwal'})
		self.assertIs(response.status_code, 200)	
	
	def test_login_unsuccessful(self):
		c = Client()
		response = c.post('/login',{'username':'spidey','password':'realoffice'})
		self.assertEqual(response.status_code, 301)	
	
	def test_add_meeting(self):
		response = self.rest_client.post('/meeting/add/', {
			'name':'meeting1',
			'organizer':'Suhaas',
			'venue' : 'DCF',
			'participants' : 'suhaas@suhaas.com',
			'date' : '2017-04-21',
			'stime' : '11:00',
			'etime' :'11:30',
			'workflow' : 'Conference'
		})

		self.assertEqual(response.status_code, 200)	
		if 'error' in response.content:
			self.fail("Error: " + response.data['error'])
	
	def test_add_meeting_without_any_clash(self):
		# Add original meeting
		self.test_add_meeting()

		# Now add next meeting
		response = self.rest_client.post('/meeting/add/', {
			'name':'meeting2',
			'organizer':'Suhaas',
			'venue' : 'CS25',
			'participants' : 'Suhaas',
			'date' : '2017-04-22',
			'stime' : '11:00',
			'etime' :'11:30',
			'workflow' : 'Conference'
		})

		self.assertEqual(response.status_code, 200)	
		if 'error' in response.content:
			self.fail("Error: " + response.data['error'])

	#time clash with meeting 2
	def test_add_meeting_withtime_clash_but_without_venue_clash(self):
		# Add original meeting
		self.test_add_meeting_without_any_clash()

		response = self.rest_client.post('/meeting/add/', {
			'name':'meeting3',
			'organizer':'Suhaas',
			'venue' : 'CS24',
			'participants' : 'Suhaas',
			'date' : '2017-04-22',
			'stime' : '11:00',
			'etime' :'11:30',
			'workflow' : 'Conference'
		})

		self.assertEqual(response.status_code, 200)	
		if 'error' in response.content:
			self.fail("Error: " + response.data['error'])

	# Clash with 1st meeting
	def test_add_meeting_clash(self):
		# Add original meeting
		self.test_add_meeting_withtime_clash_but_without_venue_clash()

		response = self.rest_client.post('/meeting/add/', {
			'name':'meeting4',
			'organizer':'Suhaas',
			'venue' : 'DCF',
			'participants' : 'Suhaas',
			'date' : '2017-04-21',
			'stime' : '11:00',
			'etime' :'11:30',
			'workflow' : 'Conference'
		})
		
		self.assertEqual(response.status_code, 200)	
		if 'error' not in response.content or response.data['error'] != 'Meeting Clash!':
			self.fail("Should have caused meeting clash!!")

	def test_add_meeting_with_Invalid_data(self):
		# Add original meetings
		self. test_add_meeting_clash()

		response = self.rest_client.post('/meeting/add/', {
			'name':'meeting5',
			'organizer':'Suhaas',
			'venue' : 'DCF',
			'participants' : 'Suhaas',
			'date' : '2017-04-21',
			'stime' : '11:30',
			'etime' :'11:00',
			'workflow' : 'Conference'
		})

		self.assertEqual(response.status_code, 200)
		if 'error' not in response.content or response.data['error'] != 'Start time >= End time!':
			self.fail("Should have caused time invalid error!!")
	
	def test_delete_existing_meeting(self):
		# Add original meetings
		self.test_add_meeting_with_Invalid_data()

		response = self.rest_client.post('/meeting/delete/', {  
			'meetingName':'meeting1'
		})

		self.assertEqual(response.status_code, 200)
		if 'error' in response.content:
			self.fail("Delete Failed!!")

	def test_delete_non_existing_meeting(self):
		# Add original meetings
		self.test_delete_existing_meeting()

		response = self.rest_client.post('/meeting/delete/', {
			'meetingName':'meeting1'
		})

		self.assertEqual(response.status_code, 200)
		if 'error' not in response.content or response.data['error'] != 'Meeting name does not exist!':
			self.fail("Delete should have failed!!")

	def test_reschedule_existing_meeting(self):
		# Add original meetings
		self.test_delete_non_existing_meeting()

		response = self.rest_client.post('/meeting/reschedule/', {  
			'name':'meeting2',
			'date':'2017-04-27',
			'stime': '11:00',
			'etime' : '12:00',
			'venue' : 'DCF'
		})
		
		self.assertEqual(response.status_code, 200)
		if 'error' in response.content:
			self.fail("Failed to reschedule!!")

	def test_reschedule_existing_meeting_adding_time_clash(self):
		# Add original meetings
		self.test_reschedule_existing_meeting()

		response = self.rest_client.post('/meeting/reschedule/', {
			'name':'meeting2',
			'date':'2017-04-22',
			'stime': '11:00',
			'etime' : '11:30',
			'venue' : 'CS24'
		})

		self.assertEqual(response.status_code, 200)
		if 'error' not in response.content or response.data['error'] != 'Meeting Clash!':
			self.fail("Should have caused clash!!")