from rest_framework import serializers
from . import models

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Resume
        fields = '__all__'

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Experience
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = '__all__' 