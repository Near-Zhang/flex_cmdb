from typing import Any
import os
from event.schedule.task import AbstractTask
from django.conf import settings
from utils import safe_json_loads, safe_json_dumps
from cloud.sdk import CloudSDKRequest, CloudSDKClient
from cloud.storage import CloudStorageEngine


__all__ = ['ResourceSyncTask']


class ResourceSyncTask(AbstractTask):
    """
    资源同步作业
    """

    def __init__(self):
        super().__init__()

        self.idc = self._params.get('idc')
        self.action = self._params.get('action')
        self.req_params = self._params.get('req_params')

    def run(self, last_result: Any = None) -> Any:
        """
        执行入库
        :param last_result: 上个作业的结果
        :return: None
        """
        # 若备用文件存在，直接使用备用文件的数据进行存储
        backup_file = self._get_backup_file()
        if os.path.exists(backup_file):
            with open(backup_file) as f:
                data = safe_json_loads(f.read())

            self._sync_to_storage(data)
            os.remove(backup_file)
            return

        # 否则使用 SDK 请求得到的数据进行存储
        client = CloudSDKClient()
        req = CloudSDKRequest(self.idc, self.action, self.req_params)
        data = client.execute(req)

        try:
            self._sync_to_storage(data)
        except Exception as e:
            with open(backup_file, 'w') as f:
                f.write(safe_json_dumps(data))
                raise e

    def _get_backup_file(self) -> str:
        """
        获取用于数据存储失败的备用文件路径
        :return: 备用文件路径
        """
        backup_file = self._params.get('backup_file')

        if backup_file:
            return backup_file
        else:
            # 目录若不存在则自动创建
            directory = f'{settings.BASE_DIR}/backup-files'
            if not os.path.exists(directory):
                os.makedirs(directory)
            return f'{directory}/{self.idc}-{self.action}'

    def _sync_to_storage(self, data) -> None:
        """
        将数据存入到存储中
        :param data: 数据
        :return: None
        """
        eg = CloudStorageEngine(self.idc, self.action)
        eg.sync(data)
