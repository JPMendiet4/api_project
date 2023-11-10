from data_api.views import CharacterList
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Tu API de Rick and Morty",
        default_version='v1',
        description="""
            Esta API se encarga de consumir cualquier API pública de preferencia, como la API de Rick and Morty, y proporciona la capacidad de filtrar los datos de la fuente seleccionada a través de no más de tres filtros. Además, ofrece una opción para que los usuarios puedan descargar la información en un archivo ZIP que contiene los datos en formato JSON.
        """,
        contact=openapi.Contact(email="juanpmendietac@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('characters/', CharacterList.as_view(), name='character-list'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
