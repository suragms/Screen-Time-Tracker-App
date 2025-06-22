from django.contrib import admin
from .models import ScreenTimeEntry
from django.utils import timezone

@admin.register(ScreenTimeEntry)
class ScreenTimeEntryAdmin(admin.ModelAdmin):
    list_display = ['activity', 'category', 'start_time', 'end_time', 'duration', 'notes', 'user']
    list_filter = ['category', 'start_time', 'user']
    search_fields = ['activity', 'notes']
    actions = ['stop_active_timers']

    def stop_active_timers(self, request, queryset):
        count = 0
        for entry in queryset.filter(end_time__isnull=True):
            entry.end_time = timezone.now()
            if entry.start_time:
                entry.duration = max(0, int((entry.end_time - entry.start_time).total_seconds() / 60))
            entry.save()
            count += 1
        self.message_user(request, f"Stopped {count} active timer(s).")
    stop_active_timers.short_description = "Stop selected active timers"