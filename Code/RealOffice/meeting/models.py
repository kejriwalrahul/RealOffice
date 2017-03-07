from __future__ import unicode_literals

# Django Stuff
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Python Libraries
from datetime import datetime


status_choices = ((1, "SCHEDULED"), (2, "RUNNING"), (3, "POST_MEETING"), (4, "FINISHED"), (5, "CANCELLED"))
rectype = ((1, "User"), (2, "Person"))

"""
	Extends the django User model
"""
class UserProfile(models.Model):
	user     = models.ForeignKey(User, on_delete= models.CASCADE)
	is_admin = models.BooleanField()

	def __str__(self):
		return self.user.username


class Venue(models.Model):
	room 			= models.CharField(max_length= 64, unique= True)
	capacity 		= models.IntegerField()
	infrastructure 	= models.CharField(max_length= 1024)

	def __str__(self):
		return self.room


class Person(models.Model):
	name  = models.CharField(max_length= 128)
	email = models.CharField(max_length= 128, unique= True)

	def __str__(self):
		return self.name


class MeetingWorkflow(models.Model):
	actions 	= models.CharField(max_length= 1024)
	meetingType = models.CharField(max_length= 64, unique= True)

	def __str__(self):
		return self.meetingType


class Meeting(models.Model):
	name 	= models.CharField(max_length= 128, unique= True)
	stime 	= models.DateTimeField()
 	etime 	= models.DateTimeField()
	status 	= models.IntegerField(choices= status_choices, default= 1)
	
	createdBy 	= models.ForeignKey(UserProfile)
	createdOn 	= models.DateTimeField(default= timezone.now)
	hostedAt  	= models.ForeignKey(Venue)
	organizedBy = models.ForeignKey(Person)
	ofType 		= models.ForeignKey(MeetingWorkflow)

	def __str__(self):
		return self.name


class Reminder(models.Model):
	recipient 	  = models.CharField(max_length= 64)
	recipientType = models.IntegerField(choices= rectype)
	purpose 	  = models.CharField(max_length= 128)
	sendDateTime  = models.DateTimeField()
	
	notificationsFor = models.ForeignKey(Meeting, on_delete= models.CASCADE)


class Requirement(models.Model):
	item = models.CharField(max_length= 128)
	qty  = models.IntegerField()
	cost = models.FloatField()
	orderDetails = models.CharField(max_length= 128, default= None, null= True)
	isApproved   = models.BooleanField()	
	
	prereqFor = models.ForeignKey(Meeting, on_delete= models.CASCADE)


class Invitation(models.Model):
	meeting = models.ForeignKey(Meeting, on_delete= models.CASCADE)
	person  = models.ForeignKey(Person, on_delete= models.CASCADE)

	willAttend = models.BooleanField()