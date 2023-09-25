from django.core import signing
from django.urls import reverse
from rest_framework import serializers
from .models import File
from django.core.exceptions import ValidationError
import os

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

    def validate_file(self, value):

        allowed_extensions = ['pptx', 'xlsx', 'docx']
        ext = os.path.splitext(value.name)[-1].lower()
        if ext not in allowed_extensions:
            raise serializers.ValidationError(
                f"Only these files: {', '.join(allowed_extensions)} are allowed."
            )
        return value

    def to_representation(self, instance):
        user = self.context['request'].user
        if user.is_ops_user:
           
            return super().to_representation(instance)
        else:
            
            encrypted_id = signing.dumps({'file_id': instance.id})
            download_url = reverse('download-file', kwargs={'token': encrypted_id})  
            return {
                'file_name': instance.file.name,
                'download_link': self.context['request'].build_absolute_uri(download_url),
            }
