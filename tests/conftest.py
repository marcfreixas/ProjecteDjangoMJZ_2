import pytest
import datetime
from django.utils import timezone
from api.models import Autor, Recurs, CategoriaRecurs


# ---------------------------------------------------------------------------
# Autor fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def autor_data():
    """Raw dict used to create an Autor — reusable in POST/PUT tests."""
    return {
        "nom": "Anna",
        "cognoms": "García López",
        "email": "anna.garcia@example.com",
        "data_naixement": datetime.date(1990, 5, 15),
        "càrrec": "Investigadora",
    }


@pytest.fixture
def autor(autor_data):
    """A persisted Autor instance."""
    return Autor.objects.create(**autor_data)


@pytest.fixture
def second_autor():
    """A second distinct Autor — useful for uniqueness / relation tests."""
    return Autor.objects.create(
        nom="Marc",
        cognoms="Martínez Puig",
        email="marc.martinez@example.com",
        data_naixement=datetime.date(1985, 8, 20),
        càrrec="Desenvolupador",
    )


# ---------------------------------------------------------------------------
# Recurs fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def recurs_data(autor):
    """Raw dict used to create a Recurs — reusable in POST/PUT tests."""
    return {
        "titol": "Introducció a Python",
        "descripcio": "Curs bàsic per aprendre Python des de zero.",
        "categoria": CategoriaRecurs.TECNOLOGIA,
        "data_publicacio": timezone.now(),
        "is_activ": True,
        "autor": autor,
    }


@pytest.fixture
def recurs(recurs_data):
    """A persisted Recurs instance."""
    return Recurs.objects.create(**recurs_data)


@pytest.fixture
def second_recurs(autor):
    """A second distinct Recurs — useful for list / filter tests."""
    return Recurs.objects.create(
        titol="Guia de Django REST Framework",
        descripcio="Com construir APIs REST amb Django.",
        categoria=CategoriaRecurs.TECNOLOGIA,
        data_publicacio=timezone.now(),
        is_activ=True,
        autor=autor,
    )
