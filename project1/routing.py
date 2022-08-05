from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from django.urls import path

from notification.consumers import NotificationConsumer
from document.consumers import MacrosConsumer


application = ProtocolTypeRouter({
    'websocket':AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                path('', NotificationConsumer()),
                path('playground/', MacrosConsumer())
            ])
        )
    )
})