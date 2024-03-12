from dukandar.models import ApniDukan
from .serializers import ApniDukanSerializer
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class ApniDukan(ViewSet) :
    permission_classes = [IsAuthenticated]

    def apniDukan(self, request) :
        apni_dukan = ApniDukan.objects.filter(slug = request.query_params.get('apniDukan'))
        serializer = ApniDukanSerializer(apni_dukan)
        return Response({'success' : True, 'data' : serializer.data})
                                              