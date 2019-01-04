from channels.routing import ProtocolTypeRouter

application = ProtocolTypeRouter({  # NOTE: What's ProtocolTypeRouter?
    # (http->django views is added by default)
})
