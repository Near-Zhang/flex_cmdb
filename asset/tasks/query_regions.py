from abc import abstractmethod
from event.job import BaseJob
from cloud.sdk import CloudSDKClient, CloudSDKRequest


class QueryRegions(BaseJob):
    """
    查询区域的任务
    """

    def __init__(self, csp):
        super().__init__()
        self._csp = csp

    @property
    def name(self):
        return f'【区域查询】{ self._csp }'

    def _run(self):
        cli = CloudSDKClient()
        req = CloudSDKRequest(self._csp, 'query_regions')
        resp = cli.execute(req)
        print(resp.data)
