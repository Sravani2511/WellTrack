from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name=""),
    path('register', views.register, name="register"),
    path('my-login', views.my_login, name="my-login"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('user-logout', views.user_logout, name="user-logout"),
    path('hydration-tracker', views.hydration_tracker, name="hydration-tracker"),  # New path for Hydration Tracker
    path('sleep-tracker', views.sleep_tracker, name="sleep-tracker"),
    path('chatbot/', views.chatbot, name='chatbot'), # New path for Sleep Tracker
    path("set_sleep_goal/", views.set_sleep_goal, name="set_sleep_goal"),
    path("log_sleep/", views.log_sleep, name="log_sleep"),
    path("get_sleep_data/", views.get_sleep_data, name="get_sleep_data"),
]
