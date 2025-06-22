from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.db.models import Sum
from .models import ScreenTimeEntry, Stopwatch, Alarm, Note, MusicPlayer, UserProfile, Song
from .forms import ScreenTimeForm, UserRegistrationForm, UserProfileForm
from rest_framework import generics
from .serializers import ScreenTimeEntrySerializer
import logging
from django.views.decorators.http import require_POST
from datetime import datetime, time, timedelta
from django.contrib.auth import login, authenticate
import json

logger = logging.getLogger(__name__)

# Existing Screen Time Views
@login_required
def list_entries(request):
    entries = ScreenTimeEntry.objects.filter(user=request.user).order_by('-start_time')
    active_timers = entries.filter(end_time__isnull=True)
    
    # Calculate total time
    total_minutes = sum(entry.duration for entry in entries if entry.duration is not None)
    total_time = timedelta(minutes=total_minutes)
    
    # Get active timer durations
    active_timer_durations = []
    for timer in active_timers:
        duration = timezone.now() - timer.start_time
        active_timer_durations.append((timer.id, duration))
    
    # Get activity data for the chart
    activity_data = list(entries.values('category').annotate(
        total_duration=Sum('duration')
    ).order_by('-total_duration'))
    
    # Format category names and handle null durations
    for item in activity_data:
        # Get the display name from choices
        category_choices = dict(ScreenTimeEntry.CATEGORY_CHOICES)
        item['category'] = category_choices.get(item['category'], item['category'])
        # Convert null duration to 0
        if item['total_duration'] is None:
            item['total_duration'] = 0
    
    # Prepare data for daily usage chart
    daily_data = []
    daily_labels = []
    for i in range(7):  # Last 7 days
        date = timezone.now().date() - timedelta(days=i)
        day_entries = entries.filter(start_time__date=date)
        total_duration = day_entries.aggregate(total=Sum('duration'))['total'] or 0
        daily_data.append(total_duration / 60)  # Convert to hours
        daily_labels.append(date.strftime('%Y-%m-%d'))
    
    # Prepare data for category distribution chart
    category_labels = [item['category'] for item in activity_data]
    category_data = [item['total_duration'] / 60 for item in activity_data]  # Convert to hours
    
    context = {
        'entries': entries,
        'total_time': total_time,
        'active_timer_durations': active_timer_durations,
        'activity_data': activity_data,
        'daily_labels': json.dumps(daily_labels),
        'daily_data': json.dumps(daily_data),
        'category_labels': json.dumps(category_labels),
        'category_data': json.dumps(category_data),
    }
    return render(request, 'list_entries.html', context)

@login_required
def add_entry(request):
    if request.method == 'POST':
        form = ScreenTimeForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.start_time = timezone.now()  # Set the start time to current time
            entry.save()
            messages.success(request, 'Screen time entry added successfully!')
            return redirect('list_entries')
    else:
        form = ScreenTimeForm()
    return render(request, 'add_entry.html', {'form': form})

@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(ScreenTimeEntry, id=entry_id, user=request.user)
    if request.method == 'POST':
        form = ScreenTimeForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Screen time entry updated successfully!')
            return redirect('list_entries')
    else:
        form = ScreenTimeForm(instance=entry)
    return render(request, 'add_entry.html', {'form': form, 'is_edit': True})

@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(ScreenTimeEntry, id=entry_id, user=request.user)
    if request.method == 'POST':
        entry.delete()
        messages.success(request, 'Screen time entry deleted successfully!')
        return redirect('list_entries')
    return redirect('list_entries')

@login_required
def stop_timer(request, entry_id):
    entry = get_object_or_404(ScreenTimeEntry, id=entry_id, user=request.user)
    if not entry.end_time:
        entry.end_time = timezone.now()
        duration = (entry.end_time - entry.start_time).total_seconds() / 60
        entry.duration = int(duration)
        entry.save()
        
        # Get category display name safely
        category_display = dict(ScreenTimeEntry.CATEGORY_CHOICES).get(entry.category, entry.category)
        
        messages.success(
            request,
            f'Timer stopped for "{entry.activity}" ({category_display}) - Duration: {entry.duration} minutes'
        )
    return redirect('list_entries')

# Stopwatch Views
@login_required
def stopwatch_list(request):
    stopwatches = Stopwatch.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'tracker/stopwatch_list.html', {'stopwatches': stopwatches})

@login_required
def stopwatch_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        stopwatch = Stopwatch.objects.create(user=request.user, name=name)
        messages.success(request, 'Stopwatch created successfully!')
        return redirect('stopwatch_list')
    return render(request, 'tracker/stopwatch_form.html')

@login_required
def stopwatch_toggle(request, pk):
    stopwatch = get_object_or_404(Stopwatch, pk=pk, user=request.user)
    if stopwatch.is_running:
        # Stop the stopwatch
        stopwatch.end_time = timezone.now()
        stopwatch.is_running = False
        if stopwatch.start_time:
            duration = (stopwatch.end_time - stopwatch.start_time).total_seconds()
            stopwatch.duration += int(duration)
    else:
        # Start the stopwatch
        stopwatch.start_time = timezone.now()
        stopwatch.is_running = True
        stopwatch.end_time = None
    stopwatch.save()
    return JsonResponse({
        'status': 'success',
        'is_running': stopwatch.is_running,
        'duration': stopwatch.duration
    })

@login_required
def stopwatch_reset(request, pk):
    stopwatch = get_object_or_404(Stopwatch, pk=pk, user=request.user)
    stopwatch.duration = 0
    stopwatch.is_running = False
    stopwatch.start_time = timezone.now()
    stopwatch.end_time = None
    stopwatch.save()
    return JsonResponse({
        'status': 'success',
        'duration': 0,
        'is_running': False
    })

@login_required
def stopwatch_delete(request, pk):
    stopwatch = get_object_or_404(Stopwatch, pk=pk, user=request.user)
    if request.method == 'POST':
        stopwatch.delete()
        messages.success(request, 'Stopwatch deleted successfully.')
        return redirect('stopwatch_list')
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

# Alarm Views
@login_required
def alarm_list(request):
    alarms = Alarm.objects.filter(user=request.user).order_by('time')
    return render(request, 'tracker/alarm_list.html', {'alarms': alarms})

@login_required
def alarm_create(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            hour = request.POST.get('hour')
            minute = request.POST.get('minute')
            period = request.POST.get('period')
            
            if not all([name, hour, minute, period]):
                messages.error(request, 'Please fill in all required fields.')
                return redirect('alarm_create')
            
            # Convert 12-hour format to 24-hour format
            hour = int(hour)
            if period == 'PM' and hour != 12:
                hour += 12
            elif period == 'AM' and hour == 12:
                hour = 0
            
            # Create time string in 24-hour format
            time_str = f"{hour:02d}:{minute}"
            
            # Create the alarm
            alarm = Alarm.objects.create(
                user=request.user,
                title=name,
                time=time_str,
                repeat='once'  # Default to once
            )
            messages.success(request, 'Alarm created successfully!')
            return redirect('alarm_list')
        except Exception as e:
            logger.error(f"Error creating alarm: {str(e)}")
            messages.error(request, 'Error creating alarm. Please try again.')
            return redirect('alarm_create')
    return render(request, 'tracker/alarm_form.html')

@login_required
def alarm_toggle(request, pk):
    alarm = get_object_or_404(Alarm, pk=pk, user=request.user)
    alarm.is_active = not alarm.is_active
    alarm.save()
    return JsonResponse({'status': 'success'})

@login_required
def alarm_update(request, alarm_id):
    alarm = get_object_or_404(Alarm, id=alarm_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        hour = request.POST.get('hour')
        minute = request.POST.get('minute')
        period = request.POST.get('period')
        
        if all([name, hour, minute, period]):
            # Convert 12-hour format to 24-hour format
            hour = int(hour)
            if period == 'PM' and hour != 12:
                hour += 12
            elif period == 'AM' and hour == 12:
                hour = 0
            
            alarm.title = name
            alarm.time = time(hour, int(minute))
            alarm.save()
            
            messages.success(request, 'Alarm updated successfully!')
            return redirect('alarm_list')
        else:
            messages.error(request, 'Please fill in all fields.')
    
    # Get current time in 12-hour format for the form
    current_hour = alarm.time.hour
    current_period = 'AM'
    
    if current_hour >= 12:
        current_period = 'PM'
        if current_hour > 12:
            current_hour -= 12
    
    context = {
        'alarm': alarm,
        'current_hour': str(current_hour),
        'current_minute': str(alarm.time.minute).zfill(2),
        'current_period': current_period
    }
    return render(request, 'tracker/alarm_form.html', context)

@require_POST
def alarm_delete(request, alarm_id):
    alarm = get_object_or_404(Alarm, id=alarm_id)
    alarm.delete()
    return JsonResponse({'status': 'success'})

# Note Views
@login_required
def note_list(request):
    notes = Note.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'tracker/note_list.html', {'notes': notes})

@login_required
def note_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        color = request.POST.get('color', '#ffffff')
        Note.objects.create(user=request.user, title=title, content=content, color=color)
        messages.success(request, 'Note created successfully!')
        return redirect('note_list')
    return render(request, 'tracker/note_form.html')

@login_required
def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        note.title = request.POST.get('title')
        note.content = request.POST.get('content')
        note.color = request.POST.get('color', note.color)
        note.save()
        messages.success(request, 'Note updated successfully!')
        return redirect('note_list')
    return render(request, 'tracker/note_form.html', {'note': note})

@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.delete()
    messages.success(request, 'Note deleted successfully!')
    return redirect('note_list')

# Music Player Views
@login_required
def music_list(request):
    songs = MusicPlayer.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'tracker/music_list.html', {
        'songs': songs
    })

@login_required
def music_upload(request):
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            artist = request.POST.get('artist')
            file = request.FILES.get('file')
            
            if not all([title, artist, file]):
                messages.error(request, 'Please fill in all fields and select a file.')
                return redirect('music_upload')
            
            if not file.content_type.startswith('audio/'):
                messages.error(request, 'Please upload a valid audio file.')
                return redirect('music_upload')
            
            song = MusicPlayer.objects.create(
                user=request.user,
                title=title,
                artist=artist,
                file=file
            )
            messages.success(request, 'Music uploaded successfully!')
            return redirect('music_list')
        except Exception as e:
            logger.error(f"Error uploading music: {str(e)}")
            messages.error(request, 'Error uploading music. Please try again.')
            return redirect('music_upload')
    return render(request, 'tracker/music_upload.html')

@login_required
def music_delete(request, pk):
    song = get_object_or_404(MusicPlayer, pk=pk, user=request.user)
    song.delete()
    messages.success(request, 'Song deleted successfully!')
    return redirect('music_list')

# API Views
class ScreenTimeEntryListCreate(generics.ListCreateAPIView):
    serializer_class = ScreenTimeEntrySerializer

    def get_queryset(self):
        return ScreenTimeEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ScreenTimeEntryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ScreenTimeEntrySerializer

    def get_queryset(self):
        return ScreenTimeEntry.objects.filter(user=self.request.user)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Screen Time Tracker.')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Get user's profile
    profile = request.user.profile
    
    # Get today's entries
    today = datetime.now().date()
    today_entries = ScreenTimeEntry.objects.filter(
        user=request.user,
        start_time__date=today
    )
    
    # Calculate today's total screen time
    today_total = today_entries.aggregate(total=Sum('duration'))['total'] or 0
    
    # Get weekly statistics
    week_start = today - timedelta(days=today.weekday())
    week_entries = ScreenTimeEntry.objects.filter(
        user=request.user,
        start_time__date__gte=week_start
    )
    
    # Calculate weekly total
    weekly_total = week_entries.aggregate(total=Sum('duration'))['total'] or 0
    
    # Get recent entries
    recent_entries = ScreenTimeEntry.objects.filter(
        user=request.user
    ).order_by('-start_time')[:5]
    
    context = {
        'profile': profile,
        'today_total': today_total,
        'weekly_total': weekly_total,
        'recent_entries': recent_entries,
        'daily_goal': profile.daily_screen_time_goal,
        'goal_percentage': min(100, (today_total / profile.daily_screen_time_goal * 100) if profile.daily_screen_time_goal > 0 else 0)
    }
    
    return render(request, 'tracker/home.html', context)

@login_required
def profile(request):
    user_profile = request.user.profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    
    context = {
        'form': form,
        'user_profile': user_profile,
    }
    return render(request, 'tracker/profile.html', context)