from urllib.parse import urlparse
from rest_framework.exceptions import ValidationError

def validate_youtube_url(value):
    parsed_url = urlparse(value)
    hostname = parsed_url.hostname

    if hostname != "youtube.com" and not (
        hostname and hostname.endswith(".youtube.com")
    ):
        raise ValidationError("Разрешены ссылки только на YouTube.")