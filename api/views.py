from api.models import Recurs, CategoriaRecurs, Autor
from rest_framework import permissions, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from api.serializers import RecursSerializer, AutorSerializer


# Class-based detail view for Recurs (GET, PUT, DELETE)
class RecursDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Recurs.objects.all()
    serializer_class = RecursSerializer
    permission_classes = [permissions.IsAuthenticated]


# Class-based list/create view for Recurs (optional, if you want separate endpoint)
class RecursListAPIView(ListCreateAPIView):
    queryset = Recurs.objects.all()
    serializer_class = RecursSerializer
    permission_classes = [permissions.IsAuthenticated]


# ViewSets for DRF router (handles GET, POST, PUT, DELETE automatically)
class RecursViewSet(viewsets.ModelViewSet):
    queryset = Recurs.objects.all()
    serializer_class = RecursSerializer
    permission_classes = [permissions.IsAuthenticated]


class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    permission_classes = [permissions.IsAuthenticated]


# APIView for CategoriaRecurs choices
class CategoriaRecursAPIView(APIView):
    permission_classes = [permissions.AllowAny]  # allow read without authentication

    def get(self, request):
        choices = [{"key": c.value, "label": c.label} for c in CategoriaRecurs]
        return Response(choices)