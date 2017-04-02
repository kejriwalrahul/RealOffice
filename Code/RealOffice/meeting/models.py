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
	user     = models.OneToOneField(User, on_delete= models.CASCADE)
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
	token	= models.CharField(max_length= 200)
	willAttend = models.BooleanField()

	def save(self):
		from django.core.mail import send_mail
		import hashlib
		hasher = hashlib.md5()
		hasher.update(self.person.name + ' ' + self.meeting.name + ' ' + str(self.meeting.stime))
		self.token = hasher.hexdigest()
		print self.token
		print type(self.token)
		mail_obj = {}
		meeting = self.meeting
		mail_obj['subject'] = 'Invitation to '+meeting.name
		mail_obj['message'] = 'Hello! You are cordially invited to '+ str(meeting.ofType) +' '+str(meeting.name) \
		+ ' organized by '+ str(meeting.organizedBy) +' set up at '+str(meeting.hostedAt)+' starting ' +str(meeting.stime)+' ending '\
		+ str(meeting.etime) + '\n\nTo accept invite, please click the url below http://localhost:8000/api/invitation/accept/?person='+str(self.person.id)+'meeting='+str(meeting.id)+'&token='\
		+ str(self.token) 
		mail_obj['sendermail'] = meeting.organizedBy.email
		mail_obj['receiver'] = self.person.email
		
		send_mail(
		    mail_obj['subject'],
		    mail_obj['message'],
		    mail_obj['sendermail'],
		    [mail_obj['receiver']],
		    fail_silently=False,
		)
		super(Invitation, self).save()