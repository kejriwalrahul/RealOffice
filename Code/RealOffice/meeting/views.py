# Django Stuff
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Rest framework stuff
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Python Libs
from datetime import datetime
from django.utils import timezone
from itertools import chain
import re
# Import Models
from models import * 

email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

"""
	For checking presence of required keys in incoming requests
"""
def check_dict(dictionary, keys):
	for key in keys:
		if key not in dictionary:
			return False

	return True


def check_person(person):
	res = {
		'unknown': [],
		'ambiguous': [],
		'known': [],
		'emails': []
	}

	persons_to_check = person.replace('[','').replace(']','').replace('"','').split(',')
	for person in persons_to_check:
		person = person.strip()

		if email_regex.match(person):
			res['emails'].append(person)
			continue

		people = Person.objects.filter(name=person)
		if not len(people):
			res['unknown'].append(person)
		elif len(people) > 1:
			res['ambiguous'].append(people[0].name)
		else:
			res['known'].append(people[0])

	return res


def loginpage(request):
	context = {}
	return render(request, 'meeting/login.html', context)


def dashboard(request):
	permission_classes = (IsAuthenticated, )
	print request.user
	reminders = Reminder.objects.filter(recipient=request.user)
	print len(reminders)
	context = {
		'username': request.user,
		'venues': Venue.objects.all(),
		'meetingWorkflows': MeetingWorkflow.objects.all(),
		'reminders' : reminders
	}
	return render(request, 'meeting/dash.html', context)

def requirement(request):
	meeting_name = request.GET['meeting']
	print meeting_name, request.user
	meeting = Meeting.objects.get(name=meeting_name)
	reminders = Reminder.objects.filter(recipient=request.user)
	print 'anon', request.user, str(request.user) == 'AnonymousUser'
	context = {
		'username': request.user,
		'meeting': meeting,
		'requirements':Requirement.objects.filter(prereqFor=meeting.id),
		'reminders' : reminders,
		'isAuthenticated' : str(request.user) != 'AnonymousUser'
	}
	return render(request, 'meeting/addreqs.html', context)


class LogOutView(APIView):
	permission_classes = (IsAuthenticated, )

	def post(self, request):
		request.user.auth_token.delete()
		return Response(status=status.HTTP_200_OK)

def meeting_summary(startdate= None, enddate= None):
	meetings = None
	if startdate:
		meetings = Meeting.objects.filter(stime__gte= startdate)
	else:
		meetings = Meeting.objects.all()
	if enddate:
		meetings.filter(etime__lte= enddate)

	meeting_info = []
	for meeting in meetings:
		if meeting.etime < timezone.now() :
			meeting.status = 4
			meeting.save()
		invitations  = Invitation.objects.filter(meeting= meeting)
		participants = [invitation.person.name for invitation in invitations]

		requirements = Requirement.objects.filter(prereqFor= meeting)
		requirements = [[requirement.item, requirement.qty, requirement.cost, requirement.isApproved] for requirement in requirements]

		invitees = Invitation.objects.filter(meeting= meeting, willAttend= True)
		headcount = len(invitees)

		meeting_info.append([
			meeting.name, meeting.stime, meeting.etime, meeting.hostedAt.room, 
			meeting.organizedBy.name, meeting.ofType.meetingType, ", ".join(participants), 
			requirements, headcount, meeting.status, meeting.createdBy.user.username, meeting.createdOn ])

	return meeting_info

class UserInfo(APIView):
	permission_classes = (IsAuthenticated,)

	def post(self, request):
		print [[r.purpose, r.notificationsFor.name] for r in Reminder.objects.filter(recipient=request.user)]
		res_data = {
			'user': unicode(request.user),
			'auth': unicode(request.auth),
			'meetings': meeting_summary(),
			'reminders': [[r.purpose, r.notificationsFor.name] for r in Reminder.objects.filter(recipient=request.user)]
		}

		return Response(res_data, status=status.HTTP_200_OK)

class Report(APIView):
	permission_classes = (IsAuthenticated, )

	def post(self, request):
		if not check_dict(request.data, ['start', 'end']):
			return Response({}, status=status.HTTP_400_BAD_REQUEST)

		res = {
			'meetings': meeting_summary(request.data['start'], request.data['end'])
		}

		return Response(res, status=status.HTTP_200_OK)

class CheckPerson(APIView):
	permission_classes = (IsAuthenticated, )

	def post(self,request):
		if not check_dict(request.data, ['persons']):
			return Response({}, status=status.HTTP_400_BAD_REQUEST)

		res = check_person(request.data['persons'])
		res.pop('known', None)
		res.pop('emails', None)

		return Response(res, status=status.HTTP_200_OK)

class AddPerson(APIView):
	permission_classes = (IsAuthenticated, )

	def post(self, request):
		if not check_dict(request.data, ['name', 'email']):
			return Response({}, status=status.HTTP_400_BAD_REQUEST)

		person_query = Person.objects.filter(email= request.data['email'])
		if person_query:
			if person_query[0].name != 'Anonymous':
				return Response({'error': 'Email already exists'}, status=status.HTTP_200_OK)
			else: 
				old_person = person_query[0]
				old_person.name = request.data['name']
				old_person.save()
		else:
			new_person = Person(name= request.data['name'], email= request.data['email'])
			new_person.save()

		return Response({}, status=status.HTTP_200_OK)

class AddMeeting(APIView):
	permission_classes = (IsAuthenticated, )

	def post(self, req):
		if not check_dict(req.data, ['name', 'organizer', 'venue', 'participants', 'date', 'stime', 'etime', 'workflow']):
			return Response({}, status=status.HTTP_400_BAD_REQUEST)

		# Validate name
		name_query = Meeting.objects.filter(name= req.data['name'])
		if name_query:
			return Response({'error': 'Meeting name already exists!'}, status=status.HTTP_200_OK)

		# Validate start and end datetimes
		stime = datetime.strptime(req.data['date'] + " " + req.data['stime'], "%Y-%m-%d %H:%M")
		etime = datetime.strptime(req.data['date'] + " " + req.data['etime'], "%Y-%m-%d %H:%M")
		if stime >= etime:
			return Response({'error': 'Start time >= End time!'}, status=status.HTTP_200_OK)

		# Validate organizer
		organizer = None
		orgres = check_person(req.data['organizer'])
		if len(orgres['unknown']) or len(orgres['ambiguous']):
			return Response({'error': 'Organizer unknown or ambiguous!'}, status=status.HTTP_200_OK)
		else:
			if (len(orgres['known']) + len(orgres['emails'])) > 1:
				return Response({'error': 'Multiple Organizers specified!'}, status=status.HTTP_200_OK)
			
			if len(orgres['known']):
				organizer = orgres['known'][0]
			else:
				person_query = Person.objects.filter(email=orgres['emails'][0])
				if person_query:
					organizer = person_query[0]
				else:
					organizer = Person(name= 'Anonymous', email= orgres['emails'][0])
					organizer.save()

		# Validate participants
		res = check_person(req.data['participants'])
		participants = res['known']
		if len(res['unknown']) or len(res['ambiguous']):
			return Response({'error': 'Organizer unknown or ambiguous!'}, status=status.HTTP_200_OK)
		else:
			if len(res['emails']):
				for email in res['emails']:
					person_query = Person.objects.filter(email=email)
					if person_query:
						participants.append(person_query[0])
					else:
						new_person = Person(name= 'Anonymous', email= email)
						new_person.save()
						participants.append(new_person)
		

		# Validate venue
		venue = None
		venue_query = Venue.objects.filter(room= req.data['venue'])
		if not venue_query:
			return Response({'error': 'Venue unknown!'}, status=status.HTTP_200_OK)
		else:
			venue = venue_query[0]

		# Validate workflow
		workflow = None
		workflow_query = MeetingWorkflow.objects.filter(meetingType= req.data['workflow'])
		if not workflow_query:
			return Response({'error': 'Workflow unknown!'}, status=status.HTTP_200_OK)
		else:
			workflow = workflow_query[0]

		# Check for clashes
		clash_meetings_bef = Meeting.objects.filter(hostedAt= venue, stime__lte= stime, etime__gte= stime)
		clash_meetings_aft = Meeting.objects.filter(hostedAt= venue, stime__lte= etime, etime__gte= etime)
		clash_meetings_dur = Meeting.objects.filter(hostedAt= venue, stime__gte= stime, etime__lte= etime)
		if clash_meetings_bef or clash_meetings_aft or clash_meetings_dur:
			clash_meetings = list(chain(clash_meetings_bef, clash_meetings_aft, clash_meetings_dur))
			clash_meetings = [ [clash.name, clash.stime, clash.etime] for clash in clash_meetings]

			return Response({ 'error': 'Meeting Clash!', 'clash': clash_meetings }, status=status.HTTP_200_OK)

		meeting = Meeting(name= req.data['name'], organizedBy= organizer, hostedAt= venue, 
						  stime= stime, etime= etime, status= 1, createdBy= req.user.userprofile, 
						  createdOn= datetime.now(), ofType= workflow)
		meeting.save()

		from django.template.loader import render_to_string
		from django.core.mail import EmailMessage
		mail_obj = {}
		# meeting = self.meeting
		mail_obj['subject'] = 'RealOffice: Meeting '+meeting.name+' created'
		mail_obj['message'] = render_to_string('organizer_mail.html', {'meeting': meeting})
		mail_obj['sendermail'] = meeting.organizedBy.email
		mail_obj['receiver'] = meeting.organizedBy.email
		msg = EmailMessage(
		    mail_obj['subject'],
		    mail_obj['message'],
		    from_email='realofficemailer@gmail.com',
		    to=[mail_obj['receiver']]
		)
		msg.content_subtype = 'html'
		msg.send()
		for participant in participants:
			Invitation(meeting= meeting, person= participant, willAttend= False).save()

		return Response({}, status=status.HTTP_200_OK)

class DeleteMeeting(APIView):
	permission_classes = (IsAuthenticated, )

	def post(self, request):
		if not check_dict(request.data, ['meetingName']):
			return Response({}, status= status.HTTP_400_BAD_REQUEST)

		meeting = Meeting.objects.filter(name= request.data['meetingName'])
		if not meeting:
			return Response({'error': 'Meeting name does not exist!'}, status= status.HTTP_200_OK)

		meeting[0].delete()

		return Response({}, status= status.HTTP_200_OK)

class RescheduleMeeting(APIView):
	permission_classes = (IsAuthenticated, )

	def post(self, request):
		if not check_dict(request.data, ['name', 'date', 'stime', 'etime', 'venue']):
			return Response({}, status= status.HTTP_400_BAD_REQUEST)

		# Validate venue
		venue = None
		venue_query = Venue.objects.filter(room= request.data['venue'])
		if not venue_query:
			return Response({'error': 'Venue unknown!'}, status=status.HTTP_200_OK)
		else:
			venue = venue_query[0]

		# Validate Times
		stime = datetime.strptime(request.data['date'] + " " + request.data['stime'], "%Y-%m-%d %H:%M")
		etime = datetime.strptime(request.data['date'] + " " + request.data['etime'], "%Y-%m-%d %H:%M")
		if stime >= etime:
			return Response({'error': 'Start time >= End time!'}, status=status.HTTP_200_OK)

		# Validate meeting
		meeting = Meeting.objects.filter(name= request.data['name'])
		if not meeting:
			return Response({'error': 'Meeting name does not exist!'}, status=status.HTTP_200_OK)
		else:
			meeting = meeting[0]

		if meeting.status == 4:
			return Response({'error': 'Meeting already over!'}, status=status.HTTP_200_OK)

		# Check for clashes
		clash_meetings_bef = Meeting.objects.filter(hostedAt= venue, stime__lte= stime, etime__gte= stime)
		clash_meetings_aft = Meeting.objects.filter(hostedAt= venue, stime__lte= etime, etime__gte= etime)
		clash_meetings_dur = Meeting.objects.filter(hostedAt= venue, stime__gte= stime, etime__lte= etime)
		if clash_meetings_bef or clash_meetings_aft or clash_meetings_dur:
			clash_meetings = list(chain(clash_meetings_bef, clash_meetings_aft, clash_meetings_dur))
			clash_meetings = [ [clash.name, clash.stime, clash.etime] for clash in clash_meetings]

			return Response({ 'error': 'Meeting Clash!', 'clash': clash_meetings }, status=status.HTTP_200_OK)

		meeting.stime = stime
		meeting.etime = etime
		meeting.hostedAt = venue
		meeting.save()

		return Response({}, status= status.HTTP_200_OK)

class ChangePassword(APIView):
	permission_classes = (IsAuthenticated, )

	def post(self, request):

		if not check_dict(request.data, ['old_pass', 'new_pass']):
			return Response({}, status=status.HTTP_400_BAD_REQUEST)

		if not request.user.check_password(request.data['old_pass']):
			return Response({}, status=status.HTTP_403_FORBIDDEN)

		request.user.set_password(request.data['new_pass'])
		request.user.save()

		return Response({}, status=status.HTTP_200_OK)

class AcceptInvitation(APIView):
	def get(self, request):
		from django.http import HttpResponse
		Invitation.objects.filter(token=request.GET['token']).update(willAttend=True)
		print len(Invitation.objects.filter(token=request.GET['token'], willAttend=True))
		return HttpResponse("<h1>Invite Accepted! Thank you for the response!</h1>")

class RequirementApprovalToggle(APIView):
	permission_classes = (IsAuthenticated, )

	def post(self, request):
		if not check_dict(request.data, ['name', 'item']):
			return Response({}, status= status.HTTP_400_BAD_REQUEST)

		req = Requirement.objects.filter(prereqFor__name= request.data['name'], item= request.data['item'])
		if not req:
			return Response({'error': 'Requirement does not exist!'}, status= status.HTTP_200_OK)
		else:
			req = req.first()

		if req.prereqFor.status == 4:
			return Response({'error': 'Meeting Already Over!'}, status= status.HTTP_200_OK)

		req.isApproved = not req.isApproved
		req.save()

		return Response({}, status= status.HTTP_200_OK)


class RequirementAdd(APIView):
	# permission_classes = (IsAuthenticated, )
	def post(self, request):
		dat = request.data
		meeting = Meeting.objects.get(name=dat['prereqFor'])
		# Requirement.objects.create(*(request.data))
		r = Requirement(item=dat['item'], qty=dat['qty'], cost=dat['cost'], prereqFor=meeting, orderDetails=dat['orderDetails'], isApproved=False)
		r.save()
		return Response(status=status.HTTP_200_OK)

class ReminderAdd(APIView):
	permission_classes = (IsAuthenticated, )
	def post(self, request):
		dat = request.data
		meeting = Meeting.objects.get(name=dat['notificationsFor'])
		# Requirement.objects.create(*(request.data))
		recipientType=1
		if dat['recipientType'] == False:
			recipientType = 2
		r = Reminder(recipient=dat['recipient'], purpose=dat['purpose'], notificationsFor=meeting, recipientType=recipientType, sendDateTime=datetime.now())
		r.save()
		return Response(status=status.HTTP_200_OK)