from django.contrib import admin

from models import * 

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Venue)
admin.site.register(Person)
admin.site.register(MeetingWorkflow)
admin.site.register(Meeting)
admin.site.register(Reminder)
admin.site.register(Requirement)
admin.site.register(Invitation)
