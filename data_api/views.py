from django.http import HttpResponse
from rest_framework import generics
from rest_framework.response import Response
import zipfile
from io import BytesIO
import json
import requests
from .models import Character
from .serializers import CharacterSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CharacterList(generics.ListAPIView):
    serializer_class = CharacterSerializer

    @swagger_auto_schema(
        operation_description="Obtener la lista de personajes de Rick and Morty.",
        manual_parameters=[
            openapi.Parameter(
                'species', openapi.IN_QUERY, description="Filtrar por especie", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'status', openapi.IN_QUERY, description="Filtrar por estado", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'download', openapi.IN_QUERY, description="Descargar datos en un archivo ZIP",
                type=openapi.TYPE_BOOLEAN
            ),
        ],
        responses={200: CharacterSerializer(many=True)},
        examples={
            'Filtrar por especie y estado': {
                'description': 'Obtener personajes de la especie "Human" y estado "Alive".',
                'value': [{'species': 'Human', 'status': 'Alive'}],
            },
            'Descargar datos en archivo ZIP': {
                'description': 'Descargar los datos en un archivo ZIP.',
                'value': {'download': True},
            },
        }
    )
    def fetch_and_store_data_from_api(self):
        api_url = "https://rickandmortyapi.com/api/character"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()

            for character_data in data.get('results', []):
                serializer = CharacterSerializer(data=character_data)
                if serializer.is_valid():
                    serializer.save()

    def get_queryset(self):
        # Consume la API de Rick and Morty y almacena los datos en la base de datos
        self.fetch_and_store_data_from_api()

        # Aplica filtros en función de los parámetros de consulta
        queryset = Character.objects.all()
        species_filter = self.request.query_params.get('species')
        status_filter = self.request.query_params.get('status')

        if species_filter:
            queryset = queryset.filter(species=species_filter)
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset

    @swagger_auto_schema(
        operation_description="Obtener la lista de personajes de Rick and Morty con filtros.",
        manual_parameters=[
            openapi.Parameter(
                'species', openapi.IN_QUERY, description="Filtrar por especie", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'status', openapi.IN_QUERY, description="Filtrar por estado", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'download', openapi.IN_QUERY, description="Descargar datos en un archivo ZIP",
                type=openapi.TYPE_BOOLEAN
            ),
        ],
        responses={200: CharacterSerializer(many=True)},
        examples={
            'Filtrar por especie y estado': {
                'description': 'Obtener personajes de la especie "Human" y estado "Alive".',
                'value': [{'species': 'Human', 'status': 'Alive'}],
            },
            'Descargar datos en archivo ZIP': {
                'description': 'Descargar los datos en un archivo ZIP.',
                'value': {'download': True},
            },
        }
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CharacterSerializer(queryset, many=True)

        if request.query_params.get('download'):
            # Prepara los datos para la descarga
            characters_data = serializer.data

            # Crea un archivo ZIP temporal y agrega los datos JSON
            buffer = BytesIO()
            with zipfile.ZipFile(buffer, 'w') as myzip:
                # Agrega los datos de la API a un archivo JSON en el ZIP
                api_url = "https://rickandmortyapi.com/api/character"
                response = requests.get(api_url)
                api_data = response.json()
                api_data_json = json.dumps(api_data, indent=4)
                myzip.writestr("api_data.json", api_data_json)

                # Agrega los datos de la base de datos a un archivo JSON en el ZIP
                db_data_json = json.dumps(characters_data, indent=4)
                myzip.writestr("database_data.json", db_data_json)

            # Configura la respuesta HTTP para descargar el archivo ZIP temporal
            buffer.seek(0)
            response = HttpResponse(buffer.read(), content_type="application/zip")
            response['Content-Disposition'] = 'attachment; filename="characters_data.zip"'

            return response

        return Response(serializer.data)
