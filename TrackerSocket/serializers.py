from rest_framework import serializers
from .models import Company, Device, Movement, Event, CustomUser


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        
        
class DeviceSerializer(serializers.ModelSerializer):
    IMEI = serializers.IntegerField(min_value=1)
    license_plate = serializers.IntegerField(min_value=1)
    company_id = serializers.PrimaryKeyRelatedField(min_value=0)
    class Meta:
        model = Device
        fields = '__all__'
    
    
class MovementSerializer(serializers.ModelSerializer):
    longitude = serializers.FloatField(min_value=0)
    latitude = serializers.FloatField(min_value=0)
    speed = serializers.FloatField(min_value=0)
    
    class Meta:
        model = Movement
        fields = '__all__'
        
        
class Event(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
    

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'company_id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            company_id=validated_data['company_id']
        )
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.company_id = validated_data.get('company_id', instance.company_id)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
