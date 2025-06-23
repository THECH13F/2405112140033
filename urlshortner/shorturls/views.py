from rest_framework import generics, permissions
from .models import ShortUrls
from .serializers import ShortUrlsSerializer
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
import requests


def get_client_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded.split(',')[0] if x_forwarded else request.META.get('REMOTE_ADDR')

class CRShortUrlsAPIView(generics.CreateAPIView):
    queryset = ShortUrls.objects.all()
    serializer_class = ShortUrlsSerializer  # ✅ Required!
    
    def post(self, request):
        serializer = ShortUrlsSerializer(data=request.data)
        if serializer.is_valid():
            ShortUrls = serializer.save()
            return Response({
                "code": ShortUrls.code,
                "original": ShortUrls.original,
                "expires_at": ShortUrls.expires_at
            })
        return Response(serializer.errors, status=400)


class RedShortUrlsAPIView(APIView):
    permission_classes = []

    def get(self, request, code):
        instance = get_object_or_404(ShortUrls, code=code)
        if instance.is_expired():
            return Response({"error": "Link expired!"}, status=410)

        # Logging to external logger service
        log_data = {
            "short_code": code,
            "accessed_at": timezone.now().isoformat(),
            "ip": get_client_ip(request),
            "user_agent": request.META.get('HTTP_USER_AGENT', '')
        }
        try:
            requests.post("http://localhost:5001/api/logs/", json=log_data)
        except requests.exceptions.RequestException:
            pass  # Do not block on logging

        return redirect(instance.original)

    