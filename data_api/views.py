from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import zipfile
from django.http import HttpResponse
from io import BytesIO
from .models import Character
from .serializers import CharacterSerializer


class AllCharacters(APIView):
    def get(self, request):
        api_url = "https://rickandmortyapi.com/api/character"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            return Response(data)
        else:
            return Response({"error": "Failed to fetch data from the API."}, status=response.status_code)


class CharacterList(generics.ListAPIView):
    serializer_class = CharacterSerializer

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

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CharacterSerializer(queryset, many=True)
        return Response(serializer.data)

    def download_data_as_zip(self, request):
        # Obtener la lista de personajes
        self.fetch_and_store_data_from_api()
        queryset = Character.objects.all()
        serializer = CharacterSerializer(queryset, many=True)
        characters_data = serializer.data

        # Crear un archivo ZIP en memoria para almacenar los datos JSON
        buffer = BytesIO()
        with zipfile.ZipFile(buffer, 'w') as zipf:
            zipf.writestr('characters.json', json.dumps(characters_data, indent=2))

        # Crear una respuesta HTTP con el archivo ZIP
        response = HttpResponse(buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=characters.zip'
        return response
