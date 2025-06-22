from django import forms
from .models import ScreenTimeEntry
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class ScreenTimeForm(forms.ModelForm):
    class Meta:
        model = ScreenTimeEntry
        fields = ['activity', 'category', 'notes']
        widgets = {
            'activity': forms.TextInput(attrs={'placeholder': 'What are you working on?', 'required': True}),
            'notes': forms.Textarea(attrs={'placeholder': 'Add any additional notes...'}),
        }

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    daily_screen_time_goal = forms.IntegerField(
        min_value=30,
        max_value=480,
        required=False,
        initial=120,
        help_text='Set your daily screen time goal (30-480 minutes)'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'bio', 'daily_screen_time_goal')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom classes and placeholders
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
        self.fields['bio'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Tell us about yourself (optional)'
        })
        self.fields['daily_screen_time_goal'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Set your daily screen time goal (minutes)'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            # Create or update user profile
            profile = UserProfile.objects.get_or_create(user=user)[0]
            profile.bio = self.cleaned_data.get('bio', '')
            profile.daily_screen_time_goal = self.cleaned_data.get('daily_screen_time_goal', 120)
            profile.save()
        
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture', 'daily_screen_time_goal', 'notification_preferences']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Tell us about yourself...'}),
            'daily_screen_time_goal': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your daily screen time goal in minutes'}),
            'notification_preferences': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }