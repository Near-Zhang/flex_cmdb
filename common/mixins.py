from typing import Optional, Union, Any
from rest_framework.response import Response
from rest_framework.views import set_rollback
from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import exceptions, status


__all__ = [
    'ListModelMixin',
    'BulkCreateModelMixin',
    'BulkUpdateModelMixin',
    'BulkDestroyModelMixin',
    'RetrieveModelMixin',
    'CreateModelMixin',
    'UpdateModelMixin',
    'DestroyModelMixin',
    'get_data_response',
    'get_error_response',
    'normalized_exception_handler'
]


def get_data_response(data: Union[dict, list, None], code: Optional[int]=200, **kwargs: Any) -> Response:
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


def normalized_exception_handler(exc: Exception, context: dict):
    """
    自定义异常处理，主要改变错误响应的格式
    """
    # 转化为 drf 设置的统一异常类
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if not isinstance(exc, exceptions.APIException):
        exc = exceptions.APIException(**exc.args)

    # 增加额外的响应头部
    headers = {}
    auth_header = getattr(exc, 'auth_header', None)
    if auth_header: headers['WWW-Authenticate'] = auth_header

    wait = getattr(exc, 'wait', None)
    if wait: headers['Retry-After'] = wait

    # 构造数据和回滚
    data = f'{exc.default_code}: {str(exc.detail)}'
    set_rollback()

    # 返回错误响应
    return get_error_response(data, code=exc.status_code, headers=headers)


##### 列表路由的处理混合 #####


class ListModelMixin:
    """
    模型对象列表查询
    """
    def list(self, request, *args, **kwargs):
        # 过滤对象
        queryset = self.filter_queryset(self.get_queryset())

        # 获取分页对象列表
        page = self.paginate_queryset(queryset)

        # 列表不为空则返回分页数据，否则返回包含所有对象的数据
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data

        # 返回响应
        return get_data_response(data)


class BulkCreateModelMixin:
    """
    单个或批量模型对象创建
    """
    def create(self, request, *args, **kwargs):
        # 若为批量操作则使用 many 参数，进行序列化
        bulk = isinstance(request.data, list)
        if not bulk:
            serializer = self.get_serializer(data=request.data)
        else:
            serializer = self.get_serializer(data=request.data, many=True)

        # 验证数据并执行创建
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # 返回响应
        return get_data_response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def perform_create(serializer):
        """
        执行创建
        """
        serializer.save()


class BulkUpdateModelMixin:
    """
    批量模型对象更新
    """
    def get_object(self):
        """
        改装获取对象的方法
        """
        # 当路由中不包含用于定位的关键字参数时，直接进行返回，否则继续正常流程
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        if lookup_url_kwarg in self.kwargs:
            return super(BulkUpdateModelMixin, self).get_object()
        return

    def bulk_update(self, request, *args, **kwargs):
        """
        批量完整更新入口，同时被部分更新所调用
        """
        # 确定是完整更新还是部分更新
        partial = kwargs.pop('partial', False)

        # 进行自定义列表序列化的序列化
        serializer = self.get_serializer(
            self.filter_queryset(self.get_queryset()),
            data=request.data,
            many=True,
            partial=partial,
        )

        # 验证数据并执行更新
        serializer.is_valid(raise_exception=True)
        self.perform_bulk_update(serializer)

        # 返回响应
        return get_data_response(serializer.data)

    def partial_bulk_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.bulk_update(request, *args, **kwargs)

    @staticmethod
    def perform_update(serializer):
        """
        执行更新
        """
        serializer.save()

    def perform_bulk_update(self, serializer):
        """
        部分更新入口
        """
        return self.perform_update(serializer)


class BulkDestroyModelMixin:
    """
    批量模型对象删除
    """

    def bulk_destroy(self, request, *args, **kwargs):
        """
        批量删除入口
        """
        # 获取和筛选查询集，并确认舒服允许批量删除
        qs = self.get_queryset()
        filtered = self.filter_queryset(qs)
        if not self.allow_bulk_destroy(qs, filtered):
            return get_error_response('not allow bulk delete', code=status.HTTP_400_BAD_REQUEST)

        # 执行批量删除
        self.perform_bulk_destroy(filtered)

        # 返回响应
        return get_data_response(None, code=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def allow_bulk_destroy(self, qs, filtered):
        """
        用于确认是否允许批量删除，若筛选后的查询集为空则返回完整查询集
        """
        return qs is not filtered

    @staticmethod
    def perform_destroy(instance):
        """
        执行单个对象删除
        """
        instance.delete()

    def perform_bulk_destroy(self, objects):
        """
        执行批量删除
        """
        for obj in objects:
            self.perform_destroy(obj)


##### 详情路由的处理混合 #####


class RetrieveModelMixin:
    """
    单个模型对象查询
    """

    def retrieve(self, request, *args, **kwargs):
        # 获取对象并序列化
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # 返回响应
        return get_data_response(serializer.data)


class CreateModelMixin:
    """
    单个模型对象创建
    """

    def create(self, request, *args, **kwargs):
        """
        单个对象创建入口
        """
        # 序列化
        serializer = self.get_serializer(data=request.data)

        # 验证数据并执行创建
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # 返回响应
        return get_data_response(serializer.data, code=status.HTTP_201_CREATED)

    @staticmethod
    def perform_create(serializer):
        """
        执行创建
        """
        serializer.save()


class UpdateModelMixin:
    """
    单个模型对象查询完整更新、部分更新
    """

    def update(self, request, *args, **kwargs):
        """
        完整更新入口，同时被部分更新所调用
        """
        # 确定是完整更新还是部分更新
        partial = kwargs.pop('partial', False)

        # 获取对象并进行序列化
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        # 验证数据并执行更新
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # 若存在预取，则清空预取缓存，
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        # 返回响应
        return get_data_response(serializer.data)

    @staticmethod
    def perform_update(serializer):
        """
        执行更新
        """
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        """
        部分更新入口
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class DestroyModelMixin:
    """
    单个模型对象删除
    """

    def destroy(self, request, *args, **kwargs):
        """
        单个对象删除入口
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return get_data_response(None, code=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def perform_destroy(instance):
        """
        执行单个对象删除
        """
        instance.delete()