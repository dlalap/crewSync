from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing
import spotcontrol.routing

# application = ProtocolTypeRouter({
#     # Empty for now (http->django views is added by default)
#     'websocket': AuthMiddlewareStack(
#         URLRouter(
#             chat.routing.websocket_urlpatterns
#         )
#     )
# })

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            spotcontrol.routing.websocket_urlpatterns
        )
    )
})