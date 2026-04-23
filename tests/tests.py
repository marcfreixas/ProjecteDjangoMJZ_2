import pytest
import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError
from api.models import Autor, Recurs, CategoriaRecurs


# ===========================================================================
# AUTOR TESTS
# ===========================================================================

@pytest.mark.django_db
class TestAutorGet:
    """Read operations for Autor."""

    def test_get_autor_by_id(self, autor):
        fetched = Autor.objects.get(id=autor.id)
        assert fetched.id == autor.id

    def test_get_autor_fields(self, autor):
        fetched = Autor.objects.get(id=autor.id)
        assert fetched.nom == "Anna"
        assert fetched.cognoms == "García López"
        assert fetched.email == "anna.garcia@example.com"
        assert fetched.data_naixement == datetime.date(1990, 5, 15)
        assert fetched.càrrec == "Investigadora"

    def test_get_autor_str(self, autor):
        assert str(autor) == "Anna García López"

    def test_get_all_autors(self, autor, second_autor):
        autors = Autor.objects.all()
        assert autors.count() == 2

    def test_get_autor_by_email(self, autor):
        fetched = Autor.objects.get(email="anna.garcia@example.com")
        assert fetched.nom == "Anna"

    def test_get_autor_not_found(self):
        with pytest.raises(Autor.DoesNotExist):
            Autor.objects.get(id=999)

    def test_get_autor_recursos(self, autor, recurs):
        """An Autor can access its related Recursos via the reverse relation."""
        assert autor.recursos.count() == 1
        assert autor.recursos.first().titol == "Introducció a Python"


@pytest.mark.django_db
class TestAutorCreate:
    """Write / update operations for Autor."""

    def test_create_autor(self, autor_data):
        autor = Autor.objects.create(**autor_data)
        assert autor.id is not None
        assert Autor.objects.count() == 1

    def test_create_autor_minimal(self):
        """Only required fields (no nullable optionals)."""
        autor = Autor.objects.create(
            nom="Pau",
            cognoms="Sánchez",
            email="pau.sanchez@example.com",
        )
        assert autor.id is not None
        assert autor.data_naixement is None
        assert autor.càrrec is None

    def test_create_autor_duplicate_email_raises(self, autor):
        with pytest.raises(Exception):  # IntegrityError from unique constraint
            Autor.objects.create(
                nom="Clon",
                cognoms="De Anna",
                email="anna.garcia@example.com",  # same email
            )

    def test_update_autor_nom(self, autor):
        autor.nom = "Anna Maria"
        autor.save()
        refreshed = Autor.objects.get(id=autor.id)
        assert refreshed.nom == "Anna Maria"

    def test_update_autor_email(self, autor):
        autor.email = "anna.new@example.com"
        autor.save()
        assert Autor.objects.get(id=autor.id).email == "anna.new@example.com"

    def test_update_autor_carrec(self, autor):
        autor.càrrec = "Directora"
        autor.save()
        assert Autor.objects.get(id=autor.id).càrrec == "Directora"

    def test_delete_autor(self, autor):
        autor_id = autor.id
        autor.delete()
        assert not Autor.objects.filter(id=autor_id).exists()

    def test_delete_autor_nullifies_recurs(self, autor, recurs):
        """Deleting an Autor sets Recurs.autor to NULL (SET_NULL)."""
        autor.delete()
        recurs.refresh_from_db()
        assert recurs.autor is None

    def test_invalid_email_raises(self):
        autor = Autor(
            nom="Invalid",
            cognoms="Email",
            email="not-an-email",
        )
        with pytest.raises(ValidationError):
            autor.full_clean()


# ===========================================================================
# RECURS TESTS
# ===========================================================================

@pytest.mark.django_db
class TestRecursGet:
    """Read operations for Recurs."""

    def test_get_recurs_by_id(self, recurs):
        fetched = Recurs.objects.get(id=recurs.id)
        assert fetched.id == recurs.id

    def test_get_recurs_fields(self, recurs):
        fetched = Recurs.objects.get(id=recurs.id)
        assert fetched.titol == "Introducció a Python"
        assert fetched.categoria == CategoriaRecurs.TECNOLOGIA
        assert fetched.is_activ is True

    def test_get_recurs_str(self, recurs):
        assert str(recurs) == "Introducció a Python"

    def test_get_all_recursos(self, recurs, second_recurs):
        assert Recurs.objects.count() == 2

    def test_get_recurs_by_categoria(self, recurs, second_recurs):
        tecnologia = Recurs.objects.filter(categoria=CategoriaRecurs.TECNOLOGIA)
        assert tecnologia.count() == 2

    def test_get_recurs_by_is_activ(self, recurs):
        actius = Recurs.objects.filter(is_activ=True)
        assert actius.count() == 1

    def test_get_recurs_not_found(self):
        with pytest.raises(Recurs.DoesNotExist):
            Recurs.objects.get(id=999)

    def test_get_recurs_autor_relation(self, recurs, autor):
        fetched = Recurs.objects.get(id=recurs.id)
        assert fetched.autor.id == autor.id
        assert fetched.autor.nom == "Anna"

    def test_get_recurs_without_autor(self):
        recurs = Recurs.objects.create(
            titol="Recurs sense autor",
            categoria=CategoriaRecurs.ALtres,
            autor=None,
        )
        assert Recurs.objects.get(id=recurs.id).autor is None

    def test_filter_recursos_by_autor(self, autor, recurs, second_recurs):
        recursos_de_autor = Recurs.objects.filter(autor=autor)
        assert recursos_de_autor.count() == 2


@pytest.mark.django_db
class TestRecursCreate:
    """Write / update operations for Recurs."""

    def test_create_recurs(self, recurs_data):
        recurs = Recurs.objects.create(**recurs_data)
        assert recurs.id is not None
        assert Recurs.objects.count() == 1

    def test_create_recurs_minimal(self):
        """Only the required field: titol."""
        recurs = Recurs.objects.create(titol="Recurs mínim")
        assert recurs.id is not None
        assert recurs.categoria == CategoriaRecurs.ALtres   # default
        assert recurs.is_activ is True                       # default
        assert recurs.autor is None

    def test_create_recurs_default_categoria(self):
        recurs = Recurs.objects.create(titol="Sense categoria")
        assert recurs.categoria == CategoriaRecurs.ALtres

    def test_create_recurs_default_is_activ(self):
        recurs = Recurs.objects.create(titol="Actiu per defecte")
        assert recurs.is_activ is True

    def test_create_recurs_all_categories(self):
        for categoria in CategoriaRecurs:
            recurs = Recurs.objects.create(
                titol=f"Recurs {categoria.label}",
                categoria=categoria,
            )
            assert recurs.categoria == categoria

    def test_update_recurs_titol(self, recurs):
        recurs.titol = "Títol actualitzat"
        recurs.save()
        assert Recurs.objects.get(id=recurs.id).titol == "Títol actualitzat"

    def test_update_recurs_categoria(self, recurs):
        recurs.categoria = CategoriaRecurs.EDUCACIO
        recurs.save()
        assert Recurs.objects.get(id=recurs.id).categoria == CategoriaRecurs.EDUCACIO

    def test_update_recurs_is_activ(self, recurs):
        recurs.is_activ = False
        recurs.save()
        assert Recurs.objects.get(id=recurs.id).is_activ is False

    def test_update_recurs_autor(self, recurs, second_autor):
        recurs.autor = second_autor
        recurs.save()
        assert Recurs.objects.get(id=recurs.id).autor.id == second_autor.id

    def test_update_recurs_remove_autor(self, recurs):
        recurs.autor = None
        recurs.save()
        assert Recurs.objects.get(id=recurs.id).autor is None

    def test_delete_recurs(self, recurs):
        recurs_id = recurs.id
        recurs.delete()
        assert not Recurs.objects.filter(id=recurs_id).exists()

    def test_titol_required(self):
        recurs = Recurs(titol="")
        with pytest.raises(ValidationError):
            recurs.full_clean()
