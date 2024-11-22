from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name=""),
    path('register', views.register, name="register"),
    path('my-login', views.my_login, name="my-login"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('user-logout', views.user_logout, name="user-logout"),
    path('hydration-tracker', views.hydration_tracker, name="hydration-tracker"),
    path('sleep-tracker', views.sleep_tracker, name="sleep-tracker"),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('calorie-tracker', views.calorie_tracker, name='calorie-tracker'),  # New path for Calorie Tracker
]
