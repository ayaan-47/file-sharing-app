

from django.urls import reverse
from rest_framework import serializers
from .models import File
from django.core import signing

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

    def to_representation(self, instance):
        user = self.context['request'].user
        if user.is_ops_user:
            # OPS users see full details and options
            return super().to_representation(instance)
        else:
            # Client users see simplified representation with encrypted download link
            encrypted_id = signing.dumps({'file_id': instance.id})
            download_url = reverse('download-file', kwargs={'token': encrypted_id})  
            return {
                'file_name': instance.file.name,
                # 'file_url': instance.file.url,
                'download_link': self.context['request'].build_absolute_uri(download_url),
            }
