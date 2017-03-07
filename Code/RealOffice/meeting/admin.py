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

class InvitationAdmin(admin.ModelAdmin):
	fieldsets = [
		('Invitation', 	{'fields': ['meeting', 'person', 'willAttend']})
	]

	list_display = ('id', 'meeting', 'person', 'willAttend')

class RequirementAdmin(admin.ModelAdmin):
	fieldsets = [
		('Prerequisite', 	{'fields': ['item', 'prereqFor', 'isApproved',]}),
		('OrderInfo', 		{'fields': ['qty', 'cost', 'orderDetails']})
	]

	list_display = ('id', 'item', 'prereqFor', 'isApproved', 'qty', 'cost', 'orderDetails')

class ReminderAdmin(admin.ModelAdmin):
	fieldsets = [
		('Recipient', 		{'fields': ['recipient', 'recipientType']}),
		('ReminderInfo', 	{'fields': ['purpose', 'sendDateTime', 'notificationsFor']})
	]

	list_display = ('id', 'recipient', 'recipientType', 'purpose', 'sendDateTime', 'notificationsFor')	

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(MeetingWorkflow, MeetingWorkflowAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Reminder, ReminderAdmin)
admin.site.register(Requirement, RequirementAdmin)
admin.site.register(Invitation, InvitationAdmin)