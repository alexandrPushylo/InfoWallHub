from django.urls import path
from presets.views import upload_preset, DeletePresetView, EditPresetView
from presets.views import ListPresetsView
from presets.views import detail_preset_view, SearchPresetsView
from presets.views import CarouselView


urlpatterns = [
    path('', CarouselView.as_view(), name="list"),
    path('library', ListPresetsView.as_view(), name="library"),
    path('private', ListPresetsView.as_view(), name="private"),
    path('<uuid:uu_id>', detail_preset_view, name="detail"),
    path('edit/<uuid:uu_id>', EditPresetView.as_view(), name="edit"),
    path('delete/<uuid:uu_id>', DeletePresetView.as_view(), name="delete"),
    path('search', SearchPresetsView.as_view(), name='search'),
    path('create/', upload_preset, name="create"),

]

