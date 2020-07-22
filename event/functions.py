from utils import ThreadBasedTimeoutControl
from .job import BaseJob
from bill.models import ExcelField


class Print(BaseJob):

    _step = (
        '第一次打印',
        '第二次打印',
        '第三次打印',
        '任务结束',
    )

    def __init__(self, k):
        super().__init__()
        self.k = k

    @property
    def name(self):
        return f'【打印信息】{self.k}'

    @ThreadBasedTimeoutControl(25)
    def _run(self):
        for i in range(3):
            self.print(i)
            self._notice_progress(0, i + 1)
        raise Exception('okok')

    def print(self, csp):
        import time
        time.sleep(10)
        print(self.k)
        ins = ExcelField.dao.create_obj(csp=csp, standard='xxx', origin='yyy')
        print(ins)
