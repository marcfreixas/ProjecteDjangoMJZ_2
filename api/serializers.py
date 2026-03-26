from api.models import Recurs, CategoriaRecurs, Autor
from rest_framework import serializers


class RecursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recurs
        fields = ["id", "titol", "descripcio", "categoria", "data_publicacio", "is_activ", "autor"]


class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ["id", "nom", "cognoms", "email", "data_naixement", "càrrec"]
