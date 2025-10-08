def after_scenario(context, scenario):
    """Cleanup після кожного сценарію"""
    if hasattr(context, 'channel'):
        context.channel.close()
    if hasattr(context, 'pc'):
        pass