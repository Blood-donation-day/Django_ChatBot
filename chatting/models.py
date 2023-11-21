from django.db import models
from accounts.models import User
from core.models import TimestampedModel

# 오늘의 요리
# 오늘 남은 질문 5

class FoodContainer(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='foods')
    filter = models.JSONField()
    foodname = models.CharField(max_length=50)
    ingredients = models.CharField(max_length=200)
    recipe = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.foodname
    

class Ticket(TimestampedModel):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='ticket')
    today_limit = models.IntegerField(default=5)
    total_used_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f'Ticket - 남은 횟수: {self.today_limit}'
