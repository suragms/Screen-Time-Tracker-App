from django.urls import path
from . import views
from . import admin_views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # Screen Time URLs
    path('', views.home, name='home'),
    path('entries/', views.list_entries, name='list_entries'),
    path('add/', views.add_entry, name='add_entry'),
    path('edit/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('delete/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    path('profile/', views.profile, name='profile'),
    path('stop/<int:entry_id>/', views.stop_timer, name='stop_timer'),
    
    # Stopwatch URLs
    path('stopwatch/', views.stopwatch_list, name='stopwatch_list'),
    path('stopwatch/create/', views.stopwatch_create, name='stopwatch_create'),
    path('stopwatch/toggle/<int:pk>/', views.stopwatch_toggle, name='stopwatch_toggle'),
    path('stopwatch/reset/<int:pk>/', views.stopwatch_reset, name='stopwatch_reset'),
    path('stopwatch/delete/<int:pk>/', views.stopwatch_delete, name='stopwatch_delete'),
    
    # Alarm URLs
    path('alarm/', views.alarm_list, name='alarm_list'),
    path('alarm/create/', views.alarm_create, name='alarm_create'),
    path('alarm/<int:alarm_id>/update/', views.alarm_update, name='alarm_update'),
    path('alarm/<int:alarm_id>/delete/', views.alarm_delete, name='alarm_delete'),
    path('alarm/<int:alarm_id>/toggle/', views.alarm_toggle, name='alarm_toggle'),
    
    # Note URLs
    path('notes/', views.note_list, name='note_list'),
    path('notes/create/', views.note_create, name='note_create'),
    path('notes/<int:pk>/update/', views.note_update, name='note_update'),
    path('notes/<int:pk>/delete/', views.note_delete, name='note_delete'),
    
    # Music Player URLs
    path('music/', views.music_list, name='music_list'),
    path('music/upload/', views.music_upload, name='music_upload'),
    path('music/<int:pk>/delete/', views.music_delete, name='music_delete'),
    
    # API URLs
    path('api/entries/', views.ScreenTimeEntryListCreate.as_view(), name='entry-list-create'),
    path('api/entries/<int:pk>/', views.ScreenTimeEntryDetail.as_view(), name='entry-detail'),
    
    # Authentication URLs
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    
    # Admin URLs
    path('admin/', admin_views.admin_redirect, name='admin_redirect'),
    path('admin/login/', admin_views.admin_login, name='admin_login'),
    path('admin/dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('admin/users/', admin_views.user_management, name='user_management'),
    path('admin/users/<int:user_id>/', admin_views.user_detail, name='user_detail'),
    path('admin/statistics/', admin_views.admin_statistics, name='admin_statistics'),
]