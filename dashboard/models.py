from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class FoodLog(models.Model):
    MEAL_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    meal = models.CharField(max_length=10, choices=MEAL_CHOICES)
    ate = models.BooleanField(default=False)
    time = models.TimeField(null=True, blank=True)  # Time of the meal

    def __str__(self):
        return f"{self.meal} on {self.date} - {'Ate' if self.ate else 'Didnt Eat'}"

class SportLog(models.Model):
    SPORT_CHOICES = [
        ('swimming', 'Swimming'),
        ('running', 'Running'),
        ('walking', 'Walking'),
        ('gym', 'Gym Session'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    did_sport = models.BooleanField(default=False)
    sport_type = models.CharField(max_length=10, choices=SPORT_CHOICES, null=True, blank=True)
    other_sport = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        if self.did_sport:
            return f"{self.get_sport_type_display()} on {self.date}"
        else:
            return f"No sport on {self.date}"
        
class SleepingLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    sleep_time = models.TimeField()
    wake_time = models.TimeField()
    woke_up_during_night = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s sleep on {self.date}"
        
class Meetings(models.Model):
    date = models.DateField()
    time = models.TimeField()
    met_people = models.BooleanField(default=False)
    positivity_rating = models.IntegerField(default=1, choices=[(i, str(i)) for i in range(1, 6)])
    meeting_types = models.ManyToManyField('MeetingType', blank=True)

    def __str__(self):
        return f"Meeting on {self.date}"

MEETING_TYPES_CHOICES = [
    ('family', 'With Family'),
    ('friends', 'With Friends'),
    ('business', 'Business Meeting'),
    ('strangers', 'With Strangers'),
    # Add more choices as needed
]

class MeetingType(models.Model):
    name = models.CharField(max_length=100, choices=MEETING_TYPES_CHOICES)

    def __str__(self):
        return self.name
    
class SeizureLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seizure_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()
    last_memory = models.TextField()

    def __str__(self):
            return f"Seizure at {self.seizure_time}"
    
class Medication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    daily_dose = models.CharField(max_length=255)
    times_per_day = models.IntegerField()

    def __str__(self):
        return self.name

class MedicationLog(models.Model):
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    date = models.DateField()
    time_taken = models.TimeField()
    feeling_after_half_hour = models.CharField(max_length=255, null=True, blank=True)
    feeling_after_one_hour = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        unique_together = ('medication', 'date', 'time_taken')

    def __str__(self):
        return f'{self.medication.name} on {self.date} at {self.time_taken}'




