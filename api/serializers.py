from api.models import Recurs, CategoriaRecurs, Autor
from rest_framework import serializers

class CategoriaRecursSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CategoriaRecurs
        fields = ["TECNOLOGIA","EDUCACIO","SALUT","ENTRETENIMENT","ALtres"]


class RecursSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Recurs
        fields = ["titol","descripcio","categoria","data_publicacio","is_activ"]


class AutorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Autor
        fields = ["nom","cognoms","email","data_naixement","càrrec"]
