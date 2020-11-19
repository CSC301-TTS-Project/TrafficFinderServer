from django.conf import settings


# TODO: ROTATE THESE DAILY
def api_keys_dict():
    return {
        'HERE_PUBLIC_KEY': settings.HERE_PUBLIC_KEY,
        'MAPBOX_PUBLIC_KEY': settings.MAPBOX_PUBLIC_KEY
    }
