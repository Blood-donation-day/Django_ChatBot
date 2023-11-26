from django.db import models
from accounts.models import User
from core.models import TimestampedModel
import os
from dotenv import load_dotenv
load_dotenv()
# 오늘의 요리
# 오늘 남은 질문 5

class FoodContainer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='foods')
    filter = models.JSONField()
    foodname = models.CharField(max_length=50)
    intro = models.CharField(max_length=200)
    ingredients = models.CharField(max_length=200)
    recipe = models.TextField()
    thumbnail = models.ImageField(upload_to='chatting/thumbnail/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.foodname


class Ticket(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ticket')
    today_limit = models.IntegerField(default=os.environ.get('TODAY_LIMIT'))
    total_used_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f'Ticket - 남은 횟수: {self.today_limit}'
