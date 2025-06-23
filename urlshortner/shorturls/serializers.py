from rest_framework import serializers
from .models import ShortUrls
from django.utils import timezone
from datetime import timedelta
import string, random

class ShortUrlsSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=False)

    class Meta:
        model = ShortUrls
        fields = ['original', 'code']

    def create(self, validated_data):
        short_code = validated_data.get('code') or self.generate_short_code()
        original_url = validated_data['original']
        expires_at = timezone.now() + timedelta(minutes=30)

        return ShortUrls.objects.create(
            original=original_url,
            code=short_code,
            expires_at=expires_at
        )

    def generate_short_code(self, length=6):
        chars = string.ascii_letters + string.digits
        while True:
            code = ''.join(random.choices(chars, k=length))
            if not ShortUrls.objects.filter(code=code).exists():
                return code
