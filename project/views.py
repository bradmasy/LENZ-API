from rest_framework.decorators import api_view
from rest_framework.response import Response

# from rest_framework.reverse import reverse


@api_view(["GET"])
def api_root(request):
    return Response(
        {
            # "users": reverse("users", request=request),
            #  "auth": reverse("auth", request=request),
        }
    )
