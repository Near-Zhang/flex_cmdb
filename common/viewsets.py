from typing import Optional, Union, Any
from rest_framework.response import Response
from rest_framework_bulk import BulkModelViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet


def get_data_response(data: Union[dict, list], code: Optional[int]=200, **kwargs: Any) -> Response:
    """
    构造返回数据的响应
    :param data: 数据
    :param code: 状态码
    :param kwargs: 包含其他响应参数的字典
    :return: 框架响应类
    """
    return Response({
        'code': code,
        'data': data,
        'message': None
    }, **kwargs)


def get_error_response(message: str, code: int, **kwargs: Any) -> Response:
    """
    构造返回错误的响应
    :param message: 错误信息
    :param code: 状态码
    :param kwargs: 包含其他响应参数的字典
    :return: 框架响应类
    """
    return Response({
        'code': code,
        'data': None,
        'message': message
    }, **kwargs)


class ReadOnlyViewSet(ReadOnlyModelViewSet):
    """
    改造了响应的只读请求视图集
    """

    def list(self, request, *args, **kwargs):
        resp = super().list(request, *args, **kwargs)
        return get_data_response(resp.data)

    def retrieve(self, request, *args, **kwargs):
        resp = super().retrieve(request, *args, **kwargs)
        return get_data_response(resp.data)


class ReadWriteViewSet(BulkModelViewSet):
    """
    改造了响应的批量处理请求视图集
    """

    def list(self, request, *args, **kwargs):
        resp = super().list(request, *args, **kwargs)
        return get_data_response(resp.data)

    def retrieve(self, request, *args, **kwargs):
        resp = super().retrieve(request, *args, **kwargs)
        return get_data_response(resp.data)

    def create(self, request, *args, **kwargs):
        resp = super().create(request, *args, **kwargs)
        return get_data_response(resp.data)

    def bulk_update(self, request, *args, **kwargs):
        resp = super().bulk_update(request, *args, **kwargs)
        return get_data_response(resp.data)

    def partial_bulk_update(self, request, *args, **kwargs):
        resp = super().partial_bulk_update(request, *args, **kwargs)
        return get_data_response(resp.data)

    def bulk_destroy(self, request, *args, **kwargs):
        resp = super().bulk_destroy(request, *args, **kwargs)
        return get_data_response(resp.data)


