from rest_framework.serializers import ModelSerializer, CharField
from utils import generate_unique_uuid
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ListSerializer, empty
from rest_framework.settings import api_settings
from rest_framework.utils import html
from collections import OrderedDict


class ResourceSerializer(ModelSerializer):
    """
    资源序列化器
    """

    uuid = CharField(max_length=32, read_only=True)
    created_by = CharField(max_length=32, read_only=True)
    updated_by = CharField(max_length=32, read_only=True)

    def validate(self, data: dict) -> dict:
        """
        全局数据认证
        :param data: 序列化传入数据
        """
        # 若序列化用于创建
        if not self.instance:
            # 不存在 UUID，则生成随机 UUID
            if not data.get('uuid'):
                data['uuid'] = generate_unique_uuid()

            # 填充创建用户 UUID
            request = self._context.get('request')
            data['created_by'] = request.user.uuid

        else:
            # 填充修改用户 UUID
            request = self._context.get('request')
            data['updated_by'] = request.user.uuid

        return data


class BulkListSerializer(ListSerializer):
    """
    批量列表序列化器，修复了 rest_framework_bulk 模块 无法处理批量更新的问题
    """
    update_lookup_field = 'id'

    def to_internal_value(self, data):
        """
        将 [{'key': 原始数据类型}, ...] 转化为 [{'key': 原生值}, ...]
        """
        if html.is_html_input(data):
            data = html.parse_html_list(data)

        if not isinstance(data, list):
            message = self.error_messages['not_a_list'].format(
                input_type=type(data).__name__
            )
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: [message]
            }, code='not_a_list')

        if not self.allow_empty and len(data) == 0:
            message = self.error_messages['empty']
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: [message]
            }, code='empty')

        # 额外区分是否为更新操作，是则组建更新实例字典
        is_update = self.instance is not None
        id_attr = 'id'
        if is_update:
            id_attr = getattr(self.child.Meta, 'update_lookup_field', 'id')
            data_by_id = {i.get(id_attr): i for i in data}
            if not all([None if id_ is empty else id_ for id_ in data_by_id.keys()]):
                raise ValidationError(f'All objects to update must have `{id_attr}`')

            instances = self.instance.filter(**{
                id_attr + '__in': data_by_id.keys(),
            })
            self.instances_by_id = OrderedDict({obj.pk: obj for obj in instances})

            if len(data_by_id) != len(self.instances_by_id):
                raise ValidationError('Could not find all objects to update.')

        ret = []
        errors = []
        for item in data:
            try:
                # 更新操作则为子序列化器对象根据上面的实例字典设置上实例属性
                if is_update:
                    id_ = item[id_attr]
                    self.child.instance = self.instances_by_id[id_]
                    validated = self.child.run_validation(item)
                    # 由于主键一般为不可写，更新操作需要手动增加到验证后的数据中
                    if not validated.get(id_attr):
                        validated[id_attr] = id_
                else:
                    validated = self.child.run_validation(item)
            except ValidationError as exc:
                errors.append(exc.detail)
            else:
                ret.append(validated)
                errors.append({})

        # 普通子序列化器对象设置上实例属性
        self.child.instance = self.instance

        if any(errors):
            raise ValidationError(errors)

        return ret

    def update(self, queryset, all_validated_data):
        id_attr = getattr(self.child.Meta, 'update_lookup_field', 'id')
        # 分离主键和验证信息
        all_validated_data_by_id = {
            i.pop(id_attr): i
            for i in all_validated_data
        }

        updated_objects = []
        for id_, obj in self.instances_by_id.items():
            obj_validated_data = all_validated_data_by_id.get(id_)

            # 子序列器执行更新操作
            updated_objects.append(
                self.child.update(obj, obj_validated_data)
            )

        return updated_objects