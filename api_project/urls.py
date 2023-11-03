from django.urls import path, include
from data_api.views import CharacterList, AllCharacters

urlpatterns = [
    path('', AllCharacters.as_view(), name='all-characters'),
    path('characters/', CharacterList.as_view(), name='character-list'),
]
