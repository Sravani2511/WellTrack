from django.db import models
from django.contrib.auth.models import User

class SleepTracker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="sleep_tracker")
    sleep_goal = models.PositiveIntegerField(default=0)  # Sleep goal in hours

    def __str__(self):
        return f"{self.user.username}'s Sleep Goal: {self.sleep_goal} hrs"

class SleepLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sleep_logs")
    date = models.DateField()
    hours = models.PositiveIntegerField()

    class Meta:
        unique_together = ('user', 'date')  # Prevent duplicate logs for the same date

    def __str__(self):
        return f"{self.user.username} - {self.date}: {self.hours} hours"
