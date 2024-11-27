from django.db import models
from django.contrib.auth.models import User

# Model for tracking calories
class CalorieLog(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='calorie_logs'
    )  # Link to the user who owns this log
    date = models.DateField()  # Date of the calorie log
    food_item = models.CharField(max_length=100, blank=True, null=True)  # Optional food item description
    calories = models.PositiveIntegerField()  # Number of calories consumed
    date_logged = models.DateTimeField(auto_now_add=True)  # Automatically log the creation timestamp

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.calories} kcal"


# Model for appointments

class Appointment(models.Model):
    name = models.CharField(max_length=100)
    appointment_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ("Pending", "Pending"), 
            ("Confirmed", "Confirmed"), 
            ("Cancelled", "Cancelled")
        ],
        default="Pending"  # Default status for appointments
    )  # Status of the appointment

    def __str__(self):
        return f"{self.name} on {self.appointment_date.strftime('%Y-%m-%d %H:%M:%S')}"
