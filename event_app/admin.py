from django.contrib import admin

from event_app.models import Event, Category, Booking, UserProfile

# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location', 'image')

# admin.site.register(Event)
admin.site.register(Category)
admin.site.register(Booking)
admin.site.register(UserProfile)
