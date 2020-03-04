from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):
    """
    认证中间件
    """

    @staticmethod
    def process_request(request):
        request.user = {
            'carrier': 'user',
            'uuid': '00000000000000000000000000000000'
        }
