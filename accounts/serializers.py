from accounts.models import User, Profile
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(validators=[validate_password])
    
    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = User(
            email=email
        )
        user.set_password(password)
        user.save()
        return user
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'profile_img', 'introduce']