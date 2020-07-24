class CloudException(Exception):
    """
    Cloud 包的总异常
    """
    pass

class CloudSDKRequestError(CloudException):
    """
    云 SDK 请求错误
    """
    pass


class CloudSDKClientError(CloudException):
    """
    云 SDK 客户端调用错误
    """
    pass


class CloudNativeSDKError(CloudException):
    """
    云原生 SDK 调用错误
    """
    pass


class CloudDataError(CloudException):
    """
    云数据错误
    """
    pass