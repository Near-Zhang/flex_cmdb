from typing import Optional, Union, Any
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework_bulk import mixins


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


class ListMixin:
    """
    处理对象列表查询请求的混合
    """

    def list(self, request, *args, **kwargs):
        # 查询集过滤
        queryset = self.filter_queryset(self.get_queryset())

        # 分页
        page = self.paginate_queryset(queryset)

        if page is not None:
            # 得到分页结果集的序列化数据
            serializer = self.get_serializer(page, many=True)
            data = self.get_paginated_response(serializer.data)
        else:
            # 得到完整结果集的序列化数据
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data

        # 返回数据
        return get_data_response(data)


class RetrieveMixin:
    """
    处理对象具体查询请求的混合
    """

    def retrieve(self, request, *args, **kwargs):
        # 获取对象
        instance = self.get_object()

        # 得到对象的序列化数据
        serializer = self.get_serializer(instance)

        # 返回数据
        return get_data_response(serializer.data)


class BulkCreateMixin(mixins.BulkCreateModelMixin):
    """
    处理对象批量创建请求的混合
    """

    def create(self, request, *args, **kwargs):
        # 根据数据是否为列表判断
        bulk = isinstance(request.data, list)

        if not bulk:
            return super().create(request, *args, **kwargs)

        else:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_bulk_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)