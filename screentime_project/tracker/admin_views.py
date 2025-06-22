from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import ScreenTimeEntry, UserProfile, Stopwatch, Alarm, Note, MusicPlayer, Song
import json

def is_admin(user):
    """Check if user is admin"""
    return user.is_authenticated and user.username == 'screentimetracker'

def admin_redirect(request):
    """Redirect to admin login or dashboard based on authentication"""
    if request.user.is_authenticated and request.user.username == 'screentimetracker':
        return redirect('admin_dashboard')
    else:
        return redirect('admin_login')

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard with overview statistics"""
    
    # Get total users
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    
    # Get users registered in last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    new_users = User.objects.filter(date_joined__gte=thirty_days_ago).count()
    
    # Get total screen time entries
    total_entries = ScreenTimeEntry.objects.count()
    
    # Get total screen time duration
    total_duration = ScreenTimeEntry.objects.aggregate(
        total=Sum('duration')
    )['total'] or 0
    
    # Get users with most screen time
    top_users = User.objects.annotate(
        total_screen_time=Sum('screentimeentry__duration')
    ).filter(total_screen_time__isnull=False).order_by('-total_screen_time')[:5]
    
    # Get recent activity
    recent_entries = ScreenTimeEntry.objects.select_related('user').order_by('-created_at')[:10]
    
    # Get category distribution
    category_stats = ScreenTimeEntry.objects.values('category').annotate(
        count=Count('id'),
        total_duration=Sum('duration')
    ).order_by('-total_duration')
    
    # Format category names
    category_choices = dict(ScreenTimeEntry.CATEGORY_CHOICES)
    for stat in category_stats:
        stat['category_name'] = category_choices.get(stat['category'], stat['category'])
    
    # Get daily user activity for last 7 days
    daily_activity = []
    for i in range(7):
        date = timezone.now().date() - timedelta(days=i)
        day_entries = ScreenTimeEntry.objects.filter(created_at__date=date)
        unique_users = day_entries.values('user').distinct().count()
        daily_activity.append({
            'date': date.strftime('%Y-%m-%d'),
            'users': unique_users,
            'entries': day_entries.count()
        })
    
    context = {
        'total_users': total_users,
        'active_users': active_users,
        'new_users': new_users,
        'total_entries': total_entries,
        'total_duration': total_duration,
        'top_users': top_users,
        'recent_entries': recent_entries,
        'category_stats': category_stats,
        'daily_activity': daily_activity,
    }
    
    return render(request, 'tracker/admin/dashboard.html', context)

def admin_login(request):
    """Custom admin login view with enhanced security"""
    # If user is already authenticated as admin, redirect to dashboard
    if request.user.is_authenticated and request.user.username == 'screentimetracker':
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Enhanced security: Only allow specific admin username
        if username == 'screentimetracker':
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_superuser:
                login(request, user)
                messages.success(request, 'Administrator access granted successfully.')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid administrator credentials. Access denied.')
        else:
            messages.error(request, 'Unauthorized access attempt. Administrator privileges required.')
    
    return render(request, 'tracker/admin/login.html')

@login_required
@user_passes_test(is_admin)
def user_management(request):
    """User management page"""
    users = User.objects.select_related('profile').order_by('-date_joined')
    
    # Get user statistics
    for user in users:
        user.total_entries = ScreenTimeEntry.objects.filter(user=user).count()
        user.total_screen_time = ScreenTimeEntry.objects.filter(user=user).aggregate(
            total=Sum('duration')
        )['total'] or 0
        user.last_login_display = user.last_login.strftime('%Y-%m-%d %H:%M') if user.last_login else 'Never'
    
    context = {
        'users': users,
    }
    
    return render(request, 'tracker/admin/user_management.html', context)

@login_required
@user_passes_test(is_admin)
def user_detail(request, user_id):
    """Detailed user information"""
    user = get_object_or_404(User, id=user_id)
    
    # Get user's screen time entries
    entries = ScreenTimeEntry.objects.filter(user=user).order_by('-created_at')
    
    # Get user's other data
    stopwatches = Stopwatch.objects.filter(user=user).count()
    alarms = Alarm.objects.filter(user=user).count()
    notes = Note.objects.filter(user=user).count()
    music_files = MusicPlayer.objects.filter(user=user).count()
    
    # Get category breakdown
    category_breakdown = entries.values('category').annotate(
        count=Count('id'),
        total_duration=Sum('duration')
    ).order_by('-total_duration')
    
    # Format category names
    category_choices = dict(ScreenTimeEntry.CATEGORY_CHOICES)
    for item in category_breakdown:
        item['category_name'] = category_choices.get(item['category'], item['category'])
    
    # Get weekly activity
    weekly_activity = []
    for i in range(7):
        date = timezone.now().date() - timedelta(days=i)
        day_entries = entries.filter(created_at__date=date)
        total_duration = day_entries.aggregate(total=Sum('duration'))['total'] or 0
        weekly_activity.append({
            'date': date.strftime('%Y-%m-%d'),
            'entries': day_entries.count(),
            'duration': total_duration
        })
    
    context = {
        'user': user,
        'entries': entries,
        'stopwatches': stopwatches,
        'alarms': alarms,
        'notes': notes,
        'music_files': music_files,
        'category_breakdown': category_breakdown,
        'weekly_activity': weekly_activity,
    }
    
    return render(request, 'tracker/admin/user_detail.html', context)

@login_required
@user_passes_test(is_admin)
def admin_statistics(request):
    """Detailed statistics page"""
    
    # User registration trends
    registration_trends = []
    for i in range(30):
        date = timezone.now().date() - timedelta(days=i)
        count = User.objects.filter(date_joined__date=date).count()
        registration_trends.append({
            'date': date.strftime('%Y-%m-%d'),
            'count': count
        })
    
    # Screen time trends
    screen_time_trends = []
    for i in range(30):
        date = timezone.now().date() - timedelta(days=i)
        total_duration = ScreenTimeEntry.objects.filter(
            created_at__date=date
        ).aggregate(total=Sum('duration'))['total'] or 0
        screen_time_trends.append({
            'date': date.strftime('%Y-%m-%d'),
            'duration': total_duration
        })
    
    # Category usage statistics
    category_usage = ScreenTimeEntry.objects.values('category').annotate(
        count=Count('id'),
        total_duration=Sum('duration'),
        avg_duration=Sum('duration') / Count('id')
    ).order_by('-total_duration')
    
    # Format category names
    category_choices = dict(ScreenTimeEntry.CATEGORY_CHOICES)
    for item in category_usage:
        item['category_name'] = category_choices.get(item['category'], item['category'])
    
    # Most active users
    most_active_users = User.objects.annotate(
        total_entries=Count('screentimeentry'),
        total_duration=Sum('screentimeentry__duration')
    ).filter(total_entries__gt=0).order_by('-total_duration')[:10]
    
    # Login statistics
    users_with_logins = User.objects.filter(last_login__isnull=False).count()
    users_never_logged_in = User.objects.filter(last_login__isnull=True).count()
    
    context = {
        'registration_trends': json.dumps(registration_trends),
        'screen_time_trends': json.dumps(screen_time_trends),
        'category_usage': category_usage,
        'most_active_users': most_active_users,
        'users_with_logins': users_with_logins,
        'users_never_logged_in': users_never_logged_in,
    }
    
    return render(request, 'tracker/admin/statistics.html', context) 