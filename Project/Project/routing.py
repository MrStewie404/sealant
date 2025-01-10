from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('api/machines/', consumers.APIMachines.as_asgi()),
    path('api/maintenance/', consumers.APIMaintenance.as_asgi()),
    path('api/claim/', consumers.APIClaim.as_asgi())
]