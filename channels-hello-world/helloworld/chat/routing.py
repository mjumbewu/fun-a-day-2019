from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    # NOTE: Uses the normal Django URL conf functions, interesting.
    url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
]
