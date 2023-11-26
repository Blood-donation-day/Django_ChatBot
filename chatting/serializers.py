from rest_framework import serializers
from .models import FoodContainer


class FoodContainerSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodContainer
        fields = ['pk', 'foodname', 'intro', 'ingredients', 'recipe', 'thumbnail', 'created_at']