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

# Import Models
from models import * 

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
		'known': []
	}

	persons_to_check = person.replace('[','').replace(']','').replace('"','').split(',')
	for person in persons_to_check:
		person = person.strip()
		people = Person.objects.filter(name=person)
		if not len(people):
			res['unknown'].append(person)
		elif len(people) > 1:
			res['ambiguous'].append(people)
		else:
			res['known'].append(people[0])

	return res


def loginpage(request):
	context = {}
	return render(request, 'meeting/login.html', context)


def dashboard(request):
	context = {
		'username': request.user,
		'venues': Venue.objects.all(),
		'meetingWorkflows': MeetingWorkflow.objects.all()
	}
	return render(request, 'meeting/dash.html', context)


class LogOutView(APIView):
	permission_classes = (IsAuthenticated, )

	def post(self, request):
		request.user.auth_token.delete()
		return Response(status=status.HTTP_200_OK)

def meeting_summary(startdate= datetime.now().date(), enddate= None):
	meetings = Meeting.objects.filter(stime__gte= startdate)
	if enddate:
		meetings.filter(etime__lte= enddate)

	meeting_info = []
	for meeting in meetings:
		invitations  = Invitation.objects.filter(meeting= meeting)
		participants = [invitation.person.name for invitation in invitations]

		requirements = Requirement.objects.filter(prereqFor= meeting)
		requirements = [[requirement.item, requirement.qty, requirement.cost, requirement.isApproved] for requirement in requirements]

		meeting_info.append([
			meeting.name, meeting.stime, meeting.etime, meeting.hostedAt.room, 
			meeting.organizedBy.name, meeting.ofType.meetingType, ", ".join(participants), requirements])

	return meeting_info

class UserInfo(APIView):
	permission_classes = (IsAuthenticated,)

	def post(self, request):
		res_data = {
			'user': unicode(request.user),
			'auth': unicode(request.auth),
			'meetings': meeting_summary()
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

		return Response(res, status=status.HTTP_200_OK)

class AddPerson(APIView):
	permission_classes = (IsAuthenticated, )

	def post(self, request):
		if not check_dict(request.data, ['name', 'email']):
			return Response({}, status=status.HTTP_400_BAD_REQUEST)

		if Person.objects.filter(email= request.data['email']):
			return Response({'error': 'Email already exists'}, status=status.HTTP_200_OK)

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
			organizer = orgres['known'][0]

		# Validate participants
		res = check_person(req.data['participants'])
		participants = res['known']
		if len(res['unknown']) or len(res['ambiguous']):
			return Response({'error': 'Organizer unknown or ambiguous!'}, status=status.HTTP_200_OK)

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
			return Response({'error': 'Meeting Clash!'}, status=status.HTTP_200_OK)

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
		    from_email=mail_obj['sendermail'],
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
		if not check_dict(request.data, ['name', 'date', 'stime', 'etime']):
			return Response({}, status= status.HTTP_400_BAD_REQUEST)

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

		# Check for clashes
		clash_meetings_bef = Meeting.objects.filter(hostedAt= meeting.hostedAt, stime__lte= stime, etime__gte= stime)
		clash_meetings_aft = Meeting.objects.filter(hostedAt= meeting.hostedAt, stime__lte= etime, etime__gte= etime)
		clash_meetings_dur = Meeting.objects.filter(hostedAt= meeting.hostedAt, stime__gte= stime, etime__lte= etime)
		if clash_meetings_bef or clash_meetings_aft or clash_meetings_dur:
			return Response({'error': 'Meeting Clash!'}, status=status.HTTP_200_OK)

		meeting.stime = stime
		meeting.etime = etime
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

		req.isApproved = not req.isApproved
		req.save()

		return Response({}, status= status.HTTP_200_OK)
