from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api import views
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# drf-yasg imports
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# DRF router
router = routers.DefaultRouter()
router.register(r"recurs", views.RecursViewSet)
router.register(r"autor", views.AutorViewSet)

# Schema view for Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="ProjecteDjangoMJZ API",
        default_version='v1',
        description="API documentation for Recurs and Autor",
        contact=openapi.Contact(email="a@a.com"),
        license=openapi.License(name="Confia bro"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("recurs/<int:id>/", views.RecursDetailAPIView.as_view(), name="recurs-detail"),
    path("categories/", views.CategoriaRecursAPIView.as_view(), name="categoria-recurs"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),

    # JWT endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # Redoc UI
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Raw JSON schema
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)