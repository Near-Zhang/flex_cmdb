from .abstract import AbstractCloudCleaner


class UCloudCleaner(AbstractCloudCleaner):
    """
    优刻得清洗器
    """

    def _clean_operation_resp(self, resp: dict) -> dict:
        """
        清洗操作类型动作的响应数据
        :param resp: 响应数据
        :return: 清洗后数据
        """
        pass

    ### 自定义的记录构建方法