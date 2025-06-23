from rest_framework import serializers
from .models import ShortUrls
from django.utils import timezone
from datetime import timedelta
import string, random

class ShortUrlsSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = ShortUrls
        fields = ['original', 'code']

    def create(self, validated_data):
        code = validated_data.get('code')

        if not code:
            code = self._generate_unique_code()
        else:
            if ShortUrls.objects.filter(code=code).exists():
                raise serializers.ValidationError({'code': 'This short code is already taken.'})

        original_url = validated_data['original']
        expires_at = timezone.now() + timedelta(minutes=30)

        return ShortUrls.objects.create(
            original=original_url,
            code=code,
            expires_at=expires_at
        )

    def _generate_unique_code(self, length=6):
        chars = string.ascii_letters + string.digits
        while True:
            code = ''.join(random.choices(chars, k=length))
            if not ShortUrls.objects.filter(code=code).exists():
                return code
