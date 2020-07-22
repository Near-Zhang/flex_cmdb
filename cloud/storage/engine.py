from typing import List, Any
from ..exceptions import *
from utils import safe_json_loads



class CloudStorageEngine:

    def __init__(self, idc_flag, cloud_action_flag :str) -> None:

        self.idc = idc_flag
        self.action = cloud_action_flag

        pass

    def sync(self, data: List[Any]) -> None:
        """
        同步数据到存储模型中，其步骤为：
        1. 检查数据符合是否标准格式
        2. 清洗数据
        3. 同步数据库
        4. 同步其他数据
        :param data: 通过云 sdk 得到的数据
        """
        if isinstance(data, list):
            raise CloudDataError("the data is not a list")

        if len(data) == 0:
            return

        self._check_standard(data)
        cleaned_data = self._clean(data)
        self._sync_to_model(cleaned_data)
        self.sync_other_data(data)

    def _check_standard(self, data: List[Any]) -> None:
        """
        检查数据符合是否标准格式
        :param data: 通过云 sdk 接口得到的数据
        """
        format = safe_json_loads(self.action.format)




        # 获取数据样本
        assert data, '传入数据为空'
        data_example = data[0]
        # 将数据key变成下划线
        new_data_example = {}
        [new_data_example.update({camel_to_underline(k): v}) for k, v in data_example.items()]
        # 获取数据有但是Model字段没有的数据
        self.different = get_model_data_different(self.action_model, **new_data_example)
        self.different = [underline_to_camel(item) for item in self.different]
        for sub_data in data:
            assert standard.keys() == sub_data.keys(), \
                '传入数据格式不对, 缺少字段: {}, 多余字段: {}'.format(
                    [i for i in standard if i not in sub_data],
                    [i for i in sub_data if i not in standard],
                )

    def _clean(self, data: List[Any]) -> List[Any]:
        new_data = []
        cloud_syncs = get_object(CloudSync, interface=self.interface.uuid, many=True)
        for sub_data in data:
            for cloud_sync in cloud_syncs:
                info = json.loads(cloud_sync.mapping)
                value = info.get(sub_data.get(cloud_sync.field))
                # 当cloud_sync默认值未none时: 记录原值
                if not value:
                    if not cloud_sync.default:
                        value = sub_data.get(cloud_sync.field)
                    else:
                        value = cloud_sync.default
                sub_data.update({
                    cloud_sync.field: value
                })
            # 驼峰变下划线
            sub_data = self.key_change_camel(sub_data)
            sub_data.update({
                'idc': self.idc.uuid
            })
            new_data.append(sub_data)
        return new_data

    def _sync_to_model(self, data: List[Any]) -> None:
        pass