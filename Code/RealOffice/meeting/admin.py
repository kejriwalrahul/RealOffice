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

	list_display = ('id', 'meetingType', 'actions')

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
		('None', 	{'fields':['name', 'organizedBy', 'ofType', 'createdBy']}),
		('When', 	{'fields':['stime', 'etime']}),
		('Where', 	{'fields':['hostedAt']}),
	]

	inlines = [ReminderInline, RequirementInline, InvitationInline]

	list_display = ('id', 'name', 'organizedBy', 'createdBy', 'ofType', 'stime', 'etime', 'hostedAt')


class UserProfileAdmin(admin.ModelAdmin):
	fieldsets = [
		('User', 	{'fields': ['user', 'is_admin']})
	]

	list_display = ('id', 'user', 'is_admin')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(MeetingWorkflow, MeetingWorkflowAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Reminder)
admin.site.register(Requirement)
admin.site.register(Invitation)