from django.db import models
from django.contrib.auth.models import User

class CalorieLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.CharField(max_length=100)
    calories = models.PositiveIntegerField()
    date_logged = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.food_item} - {self.calories} kcal"
