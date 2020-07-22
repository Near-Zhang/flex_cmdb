class CloudDataError(Exception):
    """
    云数据错误
    """
    pass


class CloudSDKRequestError(Exception):
    """
    云统一 SDK 请求错误
    """
    pass


class CloudNativeSDKError(Exception):
    """
    云原生 SDK 调用错误
    """
    pass

class CloudSDKClientError(Exception):
    """
    云 SDK 客户端调用错误
    """
    pass