from django.urls import path
from django.http import HttpResponse

from presets.views import upload_preset, DetailPresetView, DeletePresetView, EditPresetView
from presets.views import ListAllPresetsView, ListPrivatePresetsView, ListPublicPresetsView,ListPresetsView


def test(request):
    msg = "Test"
    return HttpResponse(f"{msg}\n\n{request}")


urlpatterns = [
    path('', ListPresetsView.as_view(), name="list"),
    path('library/', ListPublicPresetsView.as_view(), name="library_presets"),
    path('private/', ListPrivatePresetsView.as_view(), name="private"),

    path('<int:pk>', DetailPresetView.as_view(), name="detail"),
    path('edit/<int:pk>', EditPresetView.as_view(), name="edit"),
    path('delete/<int:pk>', DeletePresetView.as_view(), name="delete"),
    # path('search/',),
    path('create/', upload_preset, name="create"),
    # path('create/', PostCreateView.as_view(), name="create"),

]

