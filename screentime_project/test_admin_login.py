#!/usr/bin/env python
"""
Test script to verify admin login functionality
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screentime_project.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

def test_admin_login():
    """Test the admin login functionality"""
    print("Testing Admin Login Functionality")
    print("=" * 40)
    
    # Check if admin user exists
    try:
        admin_user = User.objects.get(username='screentimetracker')
        print(f"✓ Admin user '{admin_user.username}' exists")
        print(f"  - Email: {admin_user.email}")
        print(f"  - Is superuser: {admin_user.is_superuser}")
        print(f"  - Is staff: {admin_user.is_staff}")
        print(f"  - Is active: {admin_user.is_active}")
    except User.DoesNotExist:
        print("✗ Admin user 'screentimetracker' does not exist")
        print("  Run: python manage.py create_admin_user")
        return False
    
    # Test admin login page access
    client = Client()
    
    # Test accessing admin login page
    try:
        response = client.get(reverse('admin_login'))
        if response.status_code == 200:
            print("✓ Admin login page is accessible")
        else:
            print(f"✗ Admin login page returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error accessing admin login page: {e}")
        return False
    
    # Test admin redirect
    try:
        response = client.get(reverse('admin_redirect'))
        if response.status_code == 302:  # Redirect
            print("✓ Admin redirect is working")
        else:
            print(f"✗ Admin redirect returned status code: {response.status_code}")
    except Exception as e:
        print(f"✗ Error with admin redirect: {e}")
    
    # Test admin login with correct credentials
    try:
        response = client.post(reverse('admin_login'), {
            'username': 'screentimetracker',
            'password': 'Suradmin@224'
        })
        if response.status_code == 302:  # Redirect after successful login
            print("✓ Admin login with correct credentials works")
        else:
            print(f"✗ Admin login failed with status code: {response.status_code}")
    except Exception as e:
        print(f"✗ Error during admin login: {e}")
    
    print("\n" + "=" * 40)
    print("Admin login test completed!")
    return True

if __name__ == '__main__':
    test_admin_login() 