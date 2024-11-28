from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('register', views.register, name="register"),
    path('my-login', views.my_login, name="my-login"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('user-logout', views.user_logout, name="user-logout"),
    path('hydration-tracker', views.hydration_tracker, name="hydration-tracker"),
    path('sleep-tracker', views.sleep_tracker, name="sleep-tracker"),
    path('chatbot', views.chatbot, name='chatbot'),
    path('calorie-tracker', views.calorie_tracker, name='calorie-tracker'),
    path('appointment-manager', views.appointment_manager, name='appointment-manager'),  # New path for Appointment Manager
    path('add-appointment/', views.add_appointment, name='add-appointment')
    path("modify-appointment/<int:appointment_id>/", views.modify_appointment, name="modify-appointment"),
    path("delete-appointment/", views.delete_appointment, name="delete-appointment"),
    path("book-appointment/", views.confirm_appointment, name="confirm-appointment"),
    path("appointments-list/", views.appointments_list, name="appointments-list"),,
    path('add-reminder/', views.add_reminder, name='add-reminder'),
    path('book/', views.book_appointment, name='book-appointment'),
]
