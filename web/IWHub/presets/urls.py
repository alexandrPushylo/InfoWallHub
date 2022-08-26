from django.urls import path
from django.http import HttpResponse

from presets.views import upload_preset, DeletePresetView, EditPresetView
from presets.views import ListPresetsView
from presets.views import detail_preset_view, SearchPresetsView
from presets.views import CarouselView


def test(request):
    msg = "Test"
    return HttpResponse(f"{msg}\n\n{request}")


urlpatterns = [
    path('', CarouselView.as_view(), name="list"),
    # path('', ListPresetsView.as_view(), name="list"),
    path('library', ListPresetsView.as_view(), name="library"),
    path('private', ListPresetsView.as_view(), name="private"),

    # path('<int:pk>', DetailPresetView.as_view(), name="detail"),
    path('<int:pk>', detail_preset_view, name="detail"),
    path('edit/<int:pk>', EditPresetView.as_view(), name="edit"),


    path('delete/<int:pk>', DeletePresetView.as_view(), name="delete"),
    path('search', SearchPresetsView.as_view(), name='search'),
    path('create/', upload_preset, name="create"),
    # path('create/', PostCreateView.as_view(), name="create"),

]

