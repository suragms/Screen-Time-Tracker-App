from rest_framework import serializers
from .models import ScreenTimeEntry

class ScreenTimeEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreenTimeEntry
        fields = ['id', 'user', 'activity', 'category', 'notes', 'start_time', 'end_time', 'duration', 'date']
        read_only_fields = ['user', 'duration', 'date']

    def validate(self, data):
        """
        Validate that end_time is after start_time if both are provided.
        Ensure only one active timer (end_time is null) exists for a user.
        """
        if data.get('end_time') and data.get('start_time'):
            if data['end_time'] <= data['start_time']:
                raise serializers.ValidationError("End time must be after start time.")

        # Check for existing active timer if creating a new entry
        if self.context['request'].method == 'POST':
            user = self.context['request'].user
            if ScreenTimeEntry.objects.filter(user=user, end_time__isnull=True).exists():
                raise serializers.ValidationError("Cannot create new entry while a timer is active.")

        return data

    def update(self, instance, validated_data):
        """
        Custom update to handle stopping the timer (setting end_time).
        """
        if 'end_time' in validated_data and not instance.end_time:
            instance.end_time = validated_data['end_time']
            instance.save()  # Triggers duration calculation in model
        else:
            # Update other fields only if timer isn't being stopped
            for attr, value in validated_data.items():
                if attr != 'end_time':
                    setattr(instance, attr, value)
            instance.save()
        return instance