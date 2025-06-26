"""
Vistas API REST - implementación básica temporal
"""
from rest_framework.views import APIView
from rest_framework.response import Response


class TestAPIView(APIView):
    def get(self, request):
        return Response({'status': 'API working'})
