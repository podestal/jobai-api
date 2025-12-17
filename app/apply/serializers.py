from rest_framework import serializers
from . import models
from .utils import extract_text_from_file
import logging

logger = logging.getLogger(__name__)


class ResumeSerializer(serializers.ModelSerializer):
    """
    Serializer for Resume model.
    Automatically handles user assignment, text extraction, and file upload to R2.
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    file_url = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = models.Resume
        fields = ['id', 'user', 'file', 'file_url', 'text_extracted', 'created_at']
        read_only_fields = ['id', 'user', 'created_at', 'file_url', 'text_extracted']
    
    def get_file_url(self, obj):
        """Return the full URL of the uploaded file from R2"""
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None
    
    def validate_file(self, value):
        """Validate the uploaded file"""
        # Check file size (max 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        if value.size > max_size:
            raise serializers.ValidationError(
                f'File size too large. Maximum size is {max_size / (1024*1024)}MB'
            )
        
        # Check file extension
        allowed_extensions = ['.pdf', '.doc', '.docx']
        file_name = value.name.lower()
        if not any(file_name.endswith(ext) for ext in allowed_extensions):
            raise serializers.ValidationError(
                f'Invalid file type. Allowed types: {", ".join(allowed_extensions)}'
            )
        
        return value
    
    def create(self, validated_data):
        """
        Create a new resume instance.
        Extracts text from the file before saving to R2.
        """
        # Get the user from the request context
        user = self.context['request'].user
        validated_data['user'] = user
        
        # Get the file from validated_data
        file = validated_data.get('file')
        
        # Extract text from the file BEFORE saving
        # This way if extraction fails, we can still save the file
        extracted_text = ""
        if file:
            try:
                # Reset file pointer to beginning (in case it was read during validation)
                file.seek(0)
                extracted_text = extract_text_from_file(file)
                
                # Reset file pointer again after extraction (needed for saving)
                file.seek(0)
                
                if not extracted_text:
                    logger.warning(f"Text extraction returned empty for file: {file.name}")
            except Exception as e:
                logger.error(f"Error during text extraction for {file.name}: {str(e)}")
                # Continue with empty text - don't break the upload
                extracted_text = ""
        
        # Set the extracted text
        validated_data['text_extracted'] = extracted_text
        
        # File will automatically be saved to R2 via the storage backend
        return super().create(validated_data)

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Experience
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = '__all__' 