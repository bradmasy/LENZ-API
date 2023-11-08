from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(["GET"])
def api_root(request):
    return Response(
        {
            "users": reverse("users", request=request),
            "photos": reverse("photo", request=request),
            "photo-album-photos": reverse("photo-album-photo", request=request),
            "photo-albums": reverse("photo-album", request=request),
        }
    )
