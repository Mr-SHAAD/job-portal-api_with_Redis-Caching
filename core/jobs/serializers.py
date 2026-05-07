from rest_framework import serializers
from .models import Company, Job, Application
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CompanySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Company
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.ReadOnlyField(source='company.name')
    posted_by = serializers.ReadOnlyField(source='posted_by.username')

    class Meta:
        model = Job
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    applicant = serializers.ReadOnlyField(source='applicant.username')
    job_title = serializers.ReadOnlyField(source='job.title')

    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['status']