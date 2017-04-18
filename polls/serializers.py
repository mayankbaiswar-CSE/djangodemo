from django.conf.urls import url, include
from django.contrib.auth.models import User
from .models import Question, Profile
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
    
class PollSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('question', 'pub_date')

class ProfileSerialiser(serializers.ModelSerializer):
    birth_date=serializers.CharField(required=False)
    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birth_date')

class UserSerialiser(serializers.ModelSerializer):
    profile = ProfileSerialiser(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'profile')

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        profile_data = validated_data.pop('profile')
        Profile.objects.create(user=user, **profile_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


# class UserSerializer(serializers.ModelSerializer): 
#     profile = ProfileSerialiser() 
#     class Meta: 
#         model = User 
#         fields = ('username', 'email', 'profile') 
#         def create(self, validated_data): 
#             profile_data = validated_data.pop('profile') 
#             user = User.objects.create(**validated_data) 
#             Profile.objects.create(user=user, **profile_data) 
#             return user
