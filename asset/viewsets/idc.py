from rest_framework_bulk import BulkModelViewSet
from common.viewsets import ReadWriteViewSet
from ..models import IDC, Region, Zone
from ..serializers import IDCSerializer, RegionSerializer, ZoneSerializer


class IDCViewSet(ReadWriteViewSet):
    """
    供应商视图集
    """
    queryset = IDC.objects.all()
    serializer_class = IDCSerializer
    lookup_field = 'uuid'


class RegionViewSet(ReadWriteViewSet):
    """
    地域视图集
    """
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    lookup_field = 'uuid'


class ZoneViewSet(ReadWriteViewSet):
    """
    可用区视图集
    """
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
    lookup_field = 'uuid'

