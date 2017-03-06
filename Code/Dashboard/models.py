from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

# Create your models here.

status_choices = (("SCHEDULED",1), ("RUNNING",2), ("POST_MEETING",3), ("FINISHED",4), ("CANCELLED",5))
rectype = (("User",1), ("Person",2))

class UserProfile(models.Model):
	user     = models.ForeignKey(User, on_delete= models.CASCADE)
	is_admin = models.BooleanField()

class Venue(models.Model):
	room = models.CharField(max_length= 64, unique= True)
	capacity = models.IntegerField()
	infrastructure = models.CharField(max_length= 1024)

class Person(models.Model):
	name = models.CharField(max_length= 128)
	email = models.CharField(max_length= 128, unique= True)

class MeetingWorkflow(models.Model):
	actions = models.CharField(max_length= 1024)
	meetingType = models.CharField(max_length= 64, unique= True)

class Meeting(models.Model):
	name = models.CharField(max_length= 128, unique= True)
	stime = models.DateTimeField()
 	etime = models.DateTimeField()
	status = models.IntegerField(choices= status_choices)
	
	createdBy = models.ForeignKey(UserProfile)
	hostedAt = models.ForeignKey(Venue)
	organizedBy = models.ForeignKey(Person)
	ofType = models.ForeignKey(MeetingWorkflow)

class Reminder(models.Model):
	recipient = models.CharField(max_length= 64)
	recipientType = models.IntegerField(choices= rectype)
	purpose = models.CharField(max_length= 128)
	sendDateTime = models.DateTimeField()
	
	notificationsFor = models.ForeignKey(Meeting)

class Requirement(models.Model):
	item = models.CharField(max_length= 128)
	qty = models.IntegerField()
	cost = models.FloatField()
	orderDetails = models.CharField(max_length= 128)
	isApproved = models.BooleanField()	
	
	prereqFor = models.ForeignKey(Meeting)

class Invitation(models.Model):
	meetingId = models.ForeignKey(Meeting)
	personId  = models.ForeignKey(Person)

	willAttend = models.BooleanField()

