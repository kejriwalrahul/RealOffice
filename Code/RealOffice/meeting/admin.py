from django.contrib import admin
from models import *

class VenueAdmin(admin.ModelAdmin):
	fieldsets = [
		('Room Information', {'fields':['room', 'capacity', 'infrastructure']}),
	]

	list_display = ('id', 'room', 'capacity', 'infrastructure')

class PersonAdmin(admin.ModelAdmin):
	fieldsets = [
		('Person Information', {'fields':['name', 'email']}),
	]

	list_display = ('id', 'name', 'email')

class MeetingWorkflowAdmin(admin.ModelAdmin):
	fieldsets = [
		('Meeeting Workflow', {'fields':['meetingType', 'actions']}),
	]

class ReminderInline(admin.TabularInline):
	model = Reminder
	extra = 3

class RequirementInline(admin.TabularInline):
	model = Requirement
	extra = 3

class InvitationInline(admin.TabularInline):
	model = Invitation
	extra = 3

class MeetingAdmin(admin.ModelAdmin):
	fieldsets = [
		('None', 	{'fields':['name', 'organizedBy', 'ofType']}),
		('When', 	{'fields':['stime', 'etime']}),
		('Where', 	{'fields':['hostedAt']}),
	]

	inlines = [ReminderInline, RequirementInline, InvitationInline]

admin.site.register(UserProfile)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(MeetingWorkflow, MeetingWorkflowAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Reminder)
admin.site.register(Requirement)
admin.site.register(Invitation)