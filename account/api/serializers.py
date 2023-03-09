from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import Q

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        password1 = self.validated_data['password']
        password2 = self.validated_data['password2']
        queryset = User.objects.filter(Q(email=self.validated_data['email']) | Q(username=self.validated_data['username']))

        if password1 != password2:
            raise serializers.ValidationError('Passwords must match')
        
        if queryset.exists():
            raise serializers.ValidationError('Email/username already exists')
        
        user = User(email=self.validated_data['email'], username=self.validated_data['username'])
        user.set_password(self.validated_data['password2'])
        user.save()

        return user
        