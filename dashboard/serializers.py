from rest_framework import serializers
from .models import FoodLog, SportLog, SleepingLog, Meetings, MeetingType, SeizureLog, Medication, MedicationLog

class FoodLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodLog
        fields = '__all__'

class SportLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportLog
        exclude = ['meal']

class SleepingLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SleepingLog
        fields = '__all__'

class MeetingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingType
        fields = '__all__'

class MeetingsSerializer(serializers.ModelSerializer):
    meeting_types = MeetingTypeSerializer(many=True)

    class Meta:
        model = Meetings
        fields = '__all__'

    def create(self, validated_data):
        meeting_types_data = validated_data.pop('meeting_types')
        meeting = Meetings.objects.create(**validated_data)
        for meeting_type_data in meeting_types_data:
            MeetingType.objects.create(meeting=meeting, **meeting_type_data)
        return meeting

    def update(self, instance, validated_data):
        meeting_types_data = validated_data.pop('meeting_types')
        instance.date = validated_data.get('date', instance.date)
        instance.time = validated_data.get('time', instance.time)
        instance.met_people = validated_data.get('met_people', instance.met_people)
        instance.positivity_rating = validated_data.get('positivity_rating', instance.positivity_rating)
        instance.save()

        for meeting_type_data in meeting_types_data:
            meeting_type = MeetingType.objects.get(id=meeting_type_data['id'])
            meeting_type.name = meeting_type_data.get('name', meeting_type.name)
            meeting_type.save()
        
        return instance

class SeizureLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeizureLog
        fields = '__all__'

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = '__all__'

class MedicationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicationLog
        fields = '__all__'
