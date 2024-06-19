from django.utils.decorators import method_decorator
from rest_framework.views import View
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import FoodLog, SportLog, SleepingLog, Meetings, SeizureLog, Medication, MedicationLog
import json
import datetime
from .serializers import FoodLogSerializer,SportLogSerializer,SleepingLogSerializer,MeetingsSerializer,SeizureLogSerializer,MedicationSerializer, MedicationLogSerializer
from django.shortcuts import render, redirect
import requests
from django.contrib.auth.forms import UserCreationForm



# dashboard/views.py
# dashboard/views.py
import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
from .serializers import FoodLogSerializer

def dashboard_home(request, date=None):
    current_date = datetime.date.today()
    date = date or current_date.strftime('%Y-%m-%d')

    if request.method == 'POST':
        data = request.POST.dict()
        data['user'] = request.user.id
        
        serializer = FoodLogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return redirect('dashboard:dashboard_home_with_date', date=date)  # Redirect to the view with date
        else:
            return JsonResponse(serializer.errors, status=400)

    context = {}

    if date:
        api_url = f'http://localhost:8000/daily-documentation/{date}/'
        response = requests.get(api_url)
        if response.status_code == 200:
            context['documentation'] = response.json()

    context['editable'] = date == current_date.strftime('%Y-%m-%d')

    print(f"Editable: {context['editable']}")
    return render(request, 'dashboard/dashboard.html', context)




# CRUD Views for Individual Models
@method_decorator(csrf_exempt, name='dispatch')
class FoodLogView(View):
    def get(self, request):
        food_logs = FoodLog.objects.all()
        serializer = FoodLogSerializer(food_logs, many=True)
        return JsonResponse({'food_logs': serializer.data})
    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        user_id = request.user.id
        meal_type = data.get('meal')

        # Debug statement to check the user ID and meal type
        print(f"User ID: {user_id}, Meal Type: {meal_type}")

        # Check if the meal type already exists for this user
        existing_entry = FoodLog.objects.filter(user_id=user_id, meal=meal_type).first()
        if existing_entry:
            # Debug statement to indicate an existing entry
            print("Existing Entry Found")

            # Update the existing entry instead of creating a new one
            existing_entry.ate = data.get('ate', existing_entry.ate)  # Update ate field if provided
            existing_entry.time = data.get('time', existing_entry.time)  # Update time field if provided
            existing_entry.save()

            # Debug statement to confirm update
            print("Existing Entry Updated")
            return JsonResponse({'message': 'Food log updated successfully'})
        else:
            # Debug statement for creating a new entry
            print("Creating New Entry")

            # Create a new entry
            data['user_id'] = user_id
            serializer = FoodLogSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message': 'New food log created successfully'})
            else:
                return JsonResponse(serializer.errors, status=400)

    def delete(self, request, pk):
        food_log = FoodLog.objects.get(pk=pk)
        food_log.delete()
        return JsonResponse({'message': 'Food log deleted successfully'})
    

    

@method_decorator(csrf_exempt, name='dispatch')
class SportLogView(View):
    def get(self, request):
        sport_logs = SportLog.objects.all()
        serializer = SportLogSerializer(sport_logs, many=True)
        return JsonResponse({'sport_logs': serializer.data})

    def post(self, request, *args, **kwargs):
        # Assuming your form sends data in JSON format
        data = request.POST.dict()
        print("Request Data:", data)
        # Add the authenticated user's ID to the data
        data['user'] = request.user.id
        
        serializer = SportLogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return redirect('dashboard:dashboard_home', date=data['date'])
        else:
            return JsonResponse(serializer.errors, status=400)

    def put(self, request, pk):
        data = json.loads(request.body)
        sport_log = SportLog.objects.get(pk=pk)
        serializer = SportLogSerializer(sport_log, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'Sport log updated successfully'})
        return JsonResponse(serializer.errors, status=400)

    def delete(self, request, pk):
        sport_log = SportLog.objects.get(pk=pk)
        sport_log.delete()
        return JsonResponse({'message': 'Sport log deleted successfully'})
    

@method_decorator(csrf_exempt, name='dispatch')
class SleepingLogView(View):
    def get(self, request):
        sleeping_logs = SleepingLog.objects.all()
        serializer = SleepingLogSerializer(sleeping_logs, many=True)
        return JsonResponse({'sleeping_logs': serializer.data})

    def post(self, request):
        data = json.loads(request.body)
        serializer = SleepingLogSerializer(data=data)
        if serializer.is_valid():
            new_sleeping_log = serializer.save()
            return JsonResponse({'id': new_sleeping_log.id})
        return JsonResponse(serializer.errors, status=400)

    def put(self, request, pk):
        data = json.loads(request.body)
        sleeping_log = SleepingLog.objects.get(pk=pk)
        serializer = SleepingLogSerializer(sleeping_log, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'Sleeping log updated successfully'})
        return JsonResponse(serializer.errors, status=400)

    def delete(self, request, pk):
        sleeping_log = SleepingLog.objects.get(pk=pk)
        sleeping_log.delete()
        return JsonResponse({'message': 'Sleeping log deleted successfully'})


@method_decorator(csrf_exempt, name='dispatch')
class MeetingsView(View):
    def get(self, request):
        meetings = Meetings.objects.all()
        serializer = MeetingsSerializer(meetings, many=True)
        return JsonResponse({'meetings': serializer.data})

    def post(self, request):
        data = json.loads(request.body)
        serializer = MeetingsSerializer(data=data)
        if serializer.is_valid():
            new_meeting = serializer.save()
            return JsonResponse({'id': new_meeting.id})
        return JsonResponse(serializer.errors, status=400)

    def put(self, request, pk):
        data = json.loads(request.body)
        meeting = Meetings.objects.get(pk=pk)
        serializer = MeetingsSerializer(meeting, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'Meeting updated successfully'})
        return JsonResponse(serializer.errors, status=400)

    def delete(self, request, pk):
        meeting = Meetings.objects.get(pk=pk)
        meeting.delete()
        return JsonResponse({'message': 'Meeting deleted successfully'})
    

@method_decorator(csrf_exempt, name='dispatch')
class SeizureLogView(View):
    def get(self, request):
        seizure_logs = SeizureLog.objects.all()
        serializer = SeizureLogSerializer(seizure_logs, many=True)
        return JsonResponse({'seizure_logs': serializer.data})

    def post(self, request):
        data = json.loads(request.body)
        serializer = SeizureLogSerializer(data=data)
        if serializer.is_valid():
            new_seizure_log = serializer.save()
            return JsonResponse({'id': new_seizure_log.id})
        return JsonResponse(serializer.errors, status=400)

    def put(self, request, pk):
        data = json.loads(request.body)
        seizure_log = SeizureLog.objects.get(pk=pk)
        serializer = SeizureLogSerializer(seizure_log, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'Seizure log updated successfully'})
        return JsonResponse(serializer.errors, status=400)

    def delete(self, request, pk):
        seizure_log = SeizureLog.objects.get(pk=pk)
        seizure_log.delete()
        return JsonResponse({'message': 'Seizure log deleted successfully'})
    

@method_decorator(csrf_exempt, name='dispatch')
class MedicationView(View):
    def get(self, request):
        medications = Medication.objects.all()
        serializer = MedicationSerializer(medications, many=True)
        return JsonResponse({'medications': serializer.data})

    def post(self, request):
        data = json.loads(request.body)
        serializer = MedicationSerializer(data=data)
        if serializer.is_valid():
            new_medication = serializer.save()
            return JsonResponse({'id': new_medication.id})
        return JsonResponse(serializer.errors, status=400)

    def put(self, request, pk):
        data = json.loads(request.body)
        medication = Medication.objects.get(pk=pk)
        serializer = MedicationSerializer(medication, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'Medication updated successfully'})
        return JsonResponse(serializer.errors, status=400)

    def delete(self, request, pk):
        medication = Medication.objects.get(pk=pk)
        medication.delete()
        return JsonResponse({'message': 'Medication deleted successfully'})

@method_decorator(csrf_exempt, name='dispatch')
class MedicationLogView(View):
    def get(self, request):
        medication_logs = MedicationLog.objects.all()
        serializer = MedicationLogSerializer(medication_logs, many=True)
        return JsonResponse({'medication_logs': serializer.data})

    def post(self, request):
        data = json.loads(request.body)
        serializer = MedicationLogSerializer(data=data)
        if serializer.is_valid():
            new_medication_log = serializer.save()
            return JsonResponse({'id': new_medication_log.id})
        return JsonResponse(serializer.errors, status=400)

    def put(self, request, pk):
        data = json.loads(request.body)
        medication_log = MedicationLog.objects.get(pk=pk)
        serializer = MedicationLogSerializer(medication_log, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'Medication log updated successfully'})
        return JsonResponse(serializer.errors, status=400)

    def delete(self, request, pk):
        medication_log = MedicationLog.objects.get(pk=pk)
        medication_log.delete()
        return JsonResponse({'message': 'Medication log deleted successfully'})
    


# Daily Documentation View
@method_decorator(csrf_exempt, name='dispatch')
class DailyDocumentationView(View):
    def get(self, request, date):
        try:
            date_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)

        food_logs = FoodLog.objects.filter(date=date_obj)
        sport_logs = SportLog.objects.filter(date=date_obj)
        sleeping_logs = SleepingLog.objects.filter(date=date_obj)
        meetings = Meetings.objects.filter(date=date_obj)
        seizure_logs = SeizureLog.objects.filter(date=date_obj)
        medications = Medication.objects.all()  # Fetch all medications for reference

        # Serialize data
        food_logs_data = FoodLogSerializer(food_logs, many=True).data
        sport_logs_data = SportLogSerializer(sport_logs, many=True).data
        sleeping_logs_data = SleepingLogSerializer(sleeping_logs, many=True).data
        meetings_data = MeetingsSerializer(meetings, many=True).data
        seizure_logs_data = SeizureLogSerializer(seizure_logs, many=True).data
        medications_data = MedicationSerializer(medications, many=True).data

        # Construct response data
        data = {
            'date': date_obj,
            'food_logs': food_logs_data,
            'sport_logs': sport_logs_data,
            'sleeping_logs': sleeping_logs_data,
            'meetings': meetings_data,
            'seizure_logs': seizure_logs_data,
            'medications': medications_data,
            # Add more categories as needed
        }
        return JsonResponse(data)