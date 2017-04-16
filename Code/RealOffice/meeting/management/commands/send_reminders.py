from django.core.management import BaseCommand
from meeting.models import *
from datetime import datetime
#The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
	def handle(self, *args, **options):
		reminders = Reminder.objects.filter(sendDateTime__lte=datetime.now(), isReminded=False)
		reminders.update(isReminded=True)
		from django.template.loader import render_to_string
		from django.core.mail import EmailMessage
		for reminder in reminders:
			staff = User.objects.get(username='admin')
			mail_obj = {}
			mail_obj['subject'] = 'RealOffice: Reminder to '+reminder.notificationsFor.name
			mail_obj['message'] = reminder.purpose
			mail_obj['sendermail'] = 'realofficemailer@gmail.com'
			mail_obj['receiver'] = staff.email
			msg = EmailMessage(
			    mail_obj['subject'],
			    mail_obj['message'],
			    from_email=mail_obj['sendermail'],
			    to=[mail_obj['receiver']]
			)
			msg.send()