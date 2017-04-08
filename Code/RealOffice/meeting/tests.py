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
			'name':'meeting 1',
			'organizer':'Suhaas',
			'venue' : 'DCF',
			'participants' : 'Suhaas',
			'date' : '2017-04-21',
			'stime' : '11:00',
			'etime' :'11:30',
			'workflow' : 'Conference'
		})

		if 'error' in response.content:
			self.fail("Error: " + response.data['error'])

	"""
	def test_add_meeting_without_any_clash(self):
		c = Client()
		r1 =c.post('meeting/add/',{'name':'meeting 2','organizer':'Suhaas','venue' : 'CS 25','participants' : 'Suhaas','date' : '2017-04-22','stime' : '10:00','etime' :'10:30','workflow' : 'Conference'})
		if r1 == 200:
			self.assertEqual(1+1,2)

	def test_add_meeting_withtime_clash_but_without_venue_clash(self):#time clash with meeting 2
		c = Client()
		r1 =c.post('meeting/add/',{'name':'meeting 3','organizer':'Suhaas','venue' : 'CS 24','participants' : 'Suhaas','date' : '2017-04-22','stime' : '10:00','etime' :'10:30','workflow' : 'Conference'})
		if r1 == 200:
			self.assertEqual(1+1,2)

	def test_add_meeting_clash(self):
		c = Client()
		r1 =c.post('meeting/add/',{'name':'meeting 4','organizer':'Suhaas','venue' : 'DCF','participants' : 'Suhaas','date' : '2017-04-21','stime' : '11:00','etime' :'11:30','workflow' : 'Conference'})
		if r1 == 400:
			self.assertEqual(1+1,2)

	def test_add_meeting_with_Invalid_data(self):
		c = Client()
		r1 =c.post('meeting/add/',{'name':'meeting 5','organizer':'Suhaas','venue' : 'DCF','participants' : 'Suhaas','date' : '2017-04-21','stime' : '11:30','etime' :'11:00','workflow' : 'Conference'})
		if r1 == 400:
			self.assertEqual(1+1,2)
	
	def test_delete_existing_meeting(self):
		c = Client()
		r1 = r1 =c.post('meeting/delete/',{  'meetingName':'meeting 1' })
		if r1 == 200:
			self.assertEqual(1+1,2)

	def test_delete_non_existing_meeting(self):
		c = Client()
		r1 = r1 =c.post('meeting/delete/',{  'meetingName':'meeting 1' })
		if r1 == 400:
			self.assertEqual(1+1,2)

	def test_reschedule_existing_meeting(self):
		c = Client()
		r1 =c.post('meeting/reschedule/',{  'name':'meeting 2','date':'2017-04-27','stime': '11:00','etime' : '12:00' })
		if r1 == 200:
			self.assertEqual(1+1,2)

	def test_reschedule_existing_meeting_adding_time_clash(self):
		c = Client()
		r1 =c.post('meeting/add/',{'name':'meeting 5','organizer':'Suhaas','venue' : 'CS 34','participants' : 'Suhaas','date' : '2017-05-01','stime' : '10:00','etime' :'10:30','workflow' : 'Conference'})
		r2 =c.post('meeting/add/',{'name':'meeting 6','organizer':'Suhaas','venue' : 'CS 34','participants' : 'Suhaas','date' : '2017-05-01','stime' : '11:00','etime' :'11:30','workflow' : 'Conference'})	
		r3 =c.post('meeting/reschedule/',{  'name':'meeting 6','date':'2017-05-01','stime': '10:00','etime' : '10:30' })
		if r3 == 400:
			self.assertEqual(1+1,2)
	"""