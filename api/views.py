from api.models import Recurs, CategoriaRecurs, Autor
from rest_framework import permissions, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.decorators import action
from api.serializers import RecursSerializer, AutorSerializer


# Class-based detail view for Recurs (GET, PUT, DELETE)
class RecursDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Recurs.objects.all()
    serializer_class = RecursSerializer
    permission_classes = [permissions.AllowAny]


# Class-based list/create view for Recurs (optional, if you want separate endpoint)
class RecursListAPIView(ListCreateAPIView):
    queryset = Recurs.objects.all()
    serializer_class = RecursSerializer
    permission_classes = [permissions.AllowAny]


# ViewSets for DRF router (handles GET, POST, PUT, DELETE automatically)
class RecursViewSet(viewsets.ModelViewSet):
    queryset = Recurs.objects.all().order_by('id')
    serializer_class = RecursSerializer
    permission_classes = [permissions.AllowAny]


class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all().order_by('id')
    serializer_class = AutorSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['get'], url_path='recursos')
    def recursos(self, request, pk=None):
        """
        Returns all Recurs belonging to the Autor with the given id.
        GET /autors/{id}/recursos/
        """
        autor = self.get_object()  # returns 404 automatically if not found
        recursos = autor.recursos.all()
        serializer = RecursSerializer(recursos, many=True, context={'request': request})
        return Response(serializer.data)


# APIView for CategoriaRecurs choices
class CategoriaRecursAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        choices = [{"key": c.value, "label": c.label} for c in CategoriaRecurs]
        return Response(choices)
