from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings
# from kallisti import version


class InfoAPI(APIView):
    def get(self, request):
        return Response(data={
            'version': '1.0.0',  # version.VERSION,
            'platform': getattr(settings, 'KALLISTI_INFO_API_PLATFORM', {})
        })
