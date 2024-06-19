from django.urls import path
from . import views

app_name = 'dashboard'  # Define the app_name here


urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),  # Default to today's date
    path('<str:date>/', views.dashboard_home, name='dashboard_home_with_date'),
    path('food/', views.FoodLogView.as_view(), name='food-log'),
    path('food/<int:pk>/', views.FoodLogView.as_view(), name='food-log-detail'),

    path('sport/', views.SportLogView.as_view(), name='sport-log'),
    path('sport/<int:pk>/', views.SportLogView.as_view(), name='sport-log-detail'),

    path('sleep/', views.SleepingLogView.as_view(), name='sleep-log'),
    path('sleep/<int:pk>/', views.SportLogView.as_view(), name='sleep-log-detail'),

    path('meetings/', views.MeetingsView.as_view(), name='meetings'),
    path('meetings/<int:pk>/', views.MeetingsView.as_view(), name='meetings-detail'),

    path('seizure/', views.SeizureLogView.as_view(), name='seizure-log'),
    path('seizure/<int:pk>/', views.SeizureLogView.as_view(), name='seizure-log-detail'),

    path('medication/', views.MedicationView.as_view(), name='medication'),
    path('medication/<int:pk>/', views.MedicationView.as_view(), name='medication-detail'),

    path('medication-log/', views.MedicationLogView.as_view(), name='medication-log'),
    path('medication-log/<int:pk>/', views.MedicationLogView.as_view(), name='medication-log-detail'),

    path('daily-documentation/<str:date>/', views.DailyDocumentationView.as_view(), name='daily-documentation'),
]
