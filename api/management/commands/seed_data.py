import random
import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Autor, Recurs, CategoriaRecurs  # 🔁 Replace 'myapp' with your actual app name


AUTORS_DATA = [
    {"nom": "Anna",    "cognoms": "García López",     "email": "anna.garcia@example.com",    "data_naixement": datetime.date(1985, 3, 12), "càrrec": "Investigadora"},
    {"nom": "Marc",    "cognoms": "Martínez Puig",    "email": "marc.martinez@example.com",   "data_naixement": datetime.date(1990, 7, 24), "càrrec": "Desenvolupador"},
    {"nom": "Laia",    "cognoms": "Fernández Serra",  "email": "laia.fernandez@example.com",  "data_naixement": datetime.date(1988, 11, 5), "càrrec": "Dissenyadora"},
    {"nom": "Pau",     "cognoms": "Sánchez Vidal",    "email": "pau.sanchez@example.com",     "data_naixement": datetime.date(1992, 1, 30), "càrrec": "Professor"},
    {"nom": "Marta",   "cognoms": "Torres Roca",      "email": "marta.torres@example.com",    "data_naixement": datetime.date(1983, 6, 17), "càrrec": "Periodista"},
    {"nom": "Jordi",   "cognoms": "Jiménez Camps",    "email": "jordi.jimenez@example.com",   "data_naixement": datetime.date(1995, 9, 8),  "càrrec": "Enginyer"},
    {"nom": "Núria",   "cognoms": "Pérez Bosch",      "email": "nuria.perez@example.com",     "data_naixement": datetime.date(1987, 4, 22), "càrrec": "Consultora"},
    {"nom": "Àlex",    "cognoms": "Domínguez Fons",   "email": "alex.dominguez@example.com",  "data_naixement": datetime.date(1993, 12, 3), "càrrec": "Analista"},
    {"nom": "Carla",   "cognoms": "Gómez Esteve",     "email": "carla.gomez@example.com",     "data_naixement": datetime.date(1991, 8, 14), "càrrec": "Coordinadora"},
    {"nom": "Miquel",  "cognoms": "Soler Puigdomènech","email": "miquel.soler@example.com",   "data_naixement": datetime.date(1980, 2, 28), "càrrec": "Director"},
]

RECURSOS_DATA = [
    # Tecnologia
    ("Introducció a Python",              "Curs bàsic per aprendre Python des de zero.",                        CategoriaRecurs.TECNOLOGIA),
    ("Guia de Django REST Framework",     "Com construir APIs REST amb Django.",                                CategoriaRecurs.TECNOLOGIA),
    ("Docker per a desenvolupadors",      "Contenidors i orquestració amb Docker i Docker Compose.",           CategoriaRecurs.TECNOLOGIA),
    ("Fonaments de Git",                  "Control de versions amb Git i GitHub.",                             CategoriaRecurs.TECNOLOGIA),
    ("JavaScript modern (ES6+)",          "Novetats i bones pràctiques de JavaScript actual.",                 CategoriaRecurs.TECNOLOGIA),
    ("Introducció a React",               "Creació d'interfícies amb la llibreria React.",                     CategoriaRecurs.TECNOLOGIA),
    ("Bases de dades relacionals",        "SQL i disseny de bases de dades relacionals.",                      CategoriaRecurs.TECNOLOGIA),
    ("Seguretat web bàsica",              "Principals vulnerabilitats web i com prevenir-les.",                CategoriaRecurs.TECNOLOGIA),
    ("Cloud Computing amb AWS",           "Serveis essencials d'Amazon Web Services.",                         CategoriaRecurs.TECNOLOGIA),
    ("Intel·ligència artificial pràctica","Aplicació de tècniques d'IA en projectes reals.",                  CategoriaRecurs.TECNOLOGIA),
    # Educació
    ("Metodologies actives a l'aula",     "Tècniques pedagògiques per fomentar la participació.",              CategoriaRecurs.EDUCACIO),
    ("Avaluació per competències",        "Com dissenyar i aplicar avaluacions per competències.",             CategoriaRecurs.EDUCACIO),
    ("Educació inclusiva",                "Estratègies per atendre la diversitat a l'aula.",                  CategoriaRecurs.EDUCACIO),
    ("Aprenentatge basat en projectes",   "Guia pràctica per implementar l'ABP.",                             CategoriaRecurs.EDUCACIO),
    ("Eines digitals per a docents",      "Selecció d'eines TIC per millorar la docència.",                   CategoriaRecurs.EDUCACIO),
    ("Gestió emocional a l'escola",       "Recursos per treballar les emocions amb alumnes.",                  CategoriaRecurs.EDUCACIO),
    ("Educació en valors",                "Com integrar valors transversals al currículum.",                   CategoriaRecurs.EDUCACIO),
    ("Programació per a nens",            "Iniciació a la programació a primària i secundària.",               CategoriaRecurs.EDUCACIO),
    ("Flipped Classroom",                 "Model d'aula invertida: teoria i posada en pràctica.",             CategoriaRecurs.EDUCACIO),
    ("Pensament crític a l'aula",         "Activitats per desenvolupar el pensament crític.",                 CategoriaRecurs.EDUCACIO),
    # Salut
    ("Nutrició equilibrada",              "Guia pràctica per a una alimentació saludable.",                    CategoriaRecurs.SALUT),
    ("Gestió de l'estrès",                "Tècniques de relaxació i mindfulness per al dia a dia.",           CategoriaRecurs.SALUT),
    ("Activitat física i salut",          "Beneficis de l'exercici regular per a la salut.",                  CategoriaRecurs.SALUT),
    ("Salut mental en joves",             "Recursos per acompanyar joves amb dificultats emocionals.",        CategoriaRecurs.SALUT),
    ("Primers auxilis bàsics",            "Protocol d'actuació en situacions d'emergència.",                  CategoriaRecurs.SALUT),
    ("Son i descans",                     "Com millorar la qualitat del son.",                                 CategoriaRecurs.SALUT),
    ("Prevenció de l'obesitat",           "Estratègies per promoure hàbits saludables.",                      CategoriaRecurs.SALUT),
    ("Salut bucodental",                  "Consells per mantenir una bona higiene oral.",                     CategoriaRecurs.SALUT),
    ("Ergonomia a la feina",              "Com prevenir lesions musculoesquelètiques.",                        CategoriaRecurs.SALUT),
    ("Vacunació i immunitat",             "Importància de les vacunes i el calendari vacunal.",               CategoriaRecurs.SALUT),
    # Entreteniment
    ("Història del cinema",               "Evolució del setè art des dels seus orígens.",                     CategoriaRecurs.ENTRETENIMENT),
    ("Guia de viatges: Europa",           "Els destins europeus més recomanats per visitar.",                  CategoriaRecurs.ENTRETENIMENT),
    ("Introducció als escacs",            "Regles bàsiques i estratègies inicials dels escacs.",              CategoriaRecurs.ENTRETENIMENT),
    ("Lectura en català",                 "Recomanacions literàries en llengua catalana.",                    CategoriaRecurs.ENTRETENIMENT),
    ("Fotografia per a principiants",     "Composició, llum i tècnica fotogràfica bàsica.",                  CategoriaRecurs.ENTRETENIMENT),
    ("Cuina mediterrània",                "Receptes i tècniques de la cuina mediterrània tradicional.",       CategoriaRecurs.ENTRETENIMENT),
    ("Música clàssica per a tothom",      "Introducció al món de la música clàssica.",                        CategoriaRecurs.ENTRETENIMENT),
    ("Senderisme a Catalunya",            "Les millors rutes de senderisme pel territori català.",            CategoriaRecurs.ENTRETENIMENT),
    ("Aprenentatge del dibuix",           "Tècniques bàsiques per aprendre a dibuixar.",                     CategoriaRecurs.ENTRETENIMENT),
    ("Jardineria urbana",                 "Com crear un jardí en espais petits i balcons.",                   CategoriaRecurs.ENTRETENIMENT),
    # Altres
    ("Gestió del temps",                  "Mètodes per organitzar el temps de manera eficient.",              CategoriaRecurs.ALtres),
    ("Comunicació no violenta",           "Tècniques per a una comunicació més empàtica.",                    CategoriaRecurs.ALtres),
    ("Emprenedoria social",               "Com crear un projecte amb impacte social positiu.",                CategoriaRecurs.ALtres),
    ("Mediació i resolució de conflictes","Eines per gestionar conflictes de forma constructiva.",            CategoriaRecurs.ALtres),
    ("Finances personals",                "Com gestionar el pressupost i l'estalvi personal.",                CategoriaRecurs.ALtres),
    ("Voluntariat i participació cívica", "Oportunitats de voluntariat i implicació comunitària.",           CategoriaRecurs.ALtres),
    ("Llengua de signes bàsica",          "Introducció a la llengua de signes catalana.",                    CategoriaRecurs.ALtres),
    ("Sostenibilitat i medi ambient",     "Pràctiques sostenibles per reduir l'impacte ambiental.",          CategoriaRecurs.ALtres),
    ("Drets i deures dels ciutadans",     "Coneixement bàsic del marc legal i els drets fonamentals.",       CategoriaRecurs.ALtres),
    ("Introducció a la filosofia",        "Els grans corrents filosòfics occidentals.",                       CategoriaRecurs.ALtres),
]


class Command(BaseCommand):
    help = "Seed the database with 10 Autors and 50 Recursos"

    def handle(self, *args, **kwargs):
        self.stdout.write("🌱 Starting seed...")

        # --- Create Autors ---
        autors = []
        for data in AUTORS_DATA:
            autor, created = Autor.objects.get_or_create(
                email=data["email"],
                defaults={
                    "nom": data["nom"],
                    "cognoms": data["cognoms"],
                    "data_naixement": data["data_naixement"],
                    "càrrec": data["càrrec"],
                },
            )
            autors.append(autor)
            status = "✅ Created" if created else "⏭️  Already exists"
            self.stdout.write(f"  {status}: Autor '{autor}'")

        # --- Create Recursos ---
        base_date = timezone.now()
        for i, (titol, descripcio, categoria) in enumerate(RECURSOS_DATA):
            # Spread publication dates over the past ~2 years
            days_ago = random.randint(0, 730)
            data_publicacio = base_date - datetime.timedelta(days=days_ago)

            # Assign a random autor (or leave null ~20% of the time)
            autor = random.choice(autors) if random.random() > 0.2 else None

            recurs, created = Recurs.objects.get_or_create(
                titol=titol,
                defaults={
                    "descripcio": descripcio,
                    "categoria": categoria,
                    "data_publicacio": data_publicacio,
                    "is_activ": random.random() > 0.1,  # 90% active
                    "autor": autor,
                },
            )
            status = "✅ Created" if created else "⏭️  Already exists"
            self.stdout.write(f"  {status}: Recurs '{recurs}'")

        self.stdout.write(self.style.SUCCESS("\n✅ Seed completed: 10 Autors, 50 Recursos."))
