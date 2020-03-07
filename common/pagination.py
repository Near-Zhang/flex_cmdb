from typing import Optional
from django.views import View
from rest_framework.request import Request
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound
from django.core.paginator import InvalidPage
from django.db.models import QuerySet
from collections import OrderedDict


class PagePagesizePaginator(PageNumberPagination):
    """
    基于页的分页器
    """

    # 页大小参数
    page_size_query_param = 'pagesize'
    # 默认页大小
    page_size = 20
    # 最大页大小
    max_page_size = 20
    # 末尾页字符
    last_page_strings = ('last', 'end')

    def __init__(self) -> None:
        self.page = None
        self.request = None

    def paginate_queryset(self,
                          queryset: QuerySet,
                          request: Request,
                          view: Optional[View]=None) -> Optional[list]:
        """
        对查询集进行分页，成功返回数据列表，否则返回 None
        """
        # 存在 page_size 参数即启用分页
        page_number = request.query_params.get(self.page_query_param, 1)
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        # 调用 django 的分页类得到分页器
        paginator = self.django_paginator_class(queryset, page_size)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        # 获取并设定指定的页面数据，无效页面则触发异常
        try:
            page = paginator.page(page_number)
        except InvalidPage:
            raise NotFound(f'Invalid page，the page is {page_number}')

        # api 界面显示页面控制条
        if paginator.num_pages > 1 and self.template is not None:
            self.display_page_controls = True

        # 设置请求和页面属性，并返回页面数据列表
        self.request = request
        self.page = page
        return list(page)

    def get_paginated_response(self, data: list) -> OrderedDict:
        """
        得到分页后的响应数据
        """
        return OrderedDict([
            ('total', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data)
        ])