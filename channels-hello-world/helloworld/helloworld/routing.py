from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)

    # NOTE: I wonder if this is a bad idea if sessions/auth are managed in the
    # DB as opposed to a redis-like cache. And if it's fine I wonder how
    # channels gets around or justifies the blocking call.
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
