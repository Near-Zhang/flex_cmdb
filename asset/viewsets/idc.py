from rest_framework_bulk import BulkModelViewSet
from ..models import IDC, Region, Zone
from ..serializers import IDCSerializer, RegionSerializer, ZoneSerializer


class IDCViewSet(BulkModelViewSet):
    """
    供应商视图集
    """
    queryset = IDC.objects.all()
    serializer_class = IDCSerializer
    lookup_field = 'uuid'


class RegionViewSet(BulkModelViewSet):
    """
    地域视图集
    """
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    lookup_field = 'uuid'


class ZoneViewSet(BulkModelViewSet):
    """
    可用区视图集
    """
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
    lookup_field = 'uuid'

