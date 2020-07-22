from channels.generic.websocket import AsyncWebsocketConsumer
from utils import safe_json_dumps


class JobConsumer(AsyncWebsocketConsumer):
    """
    当 job 处理完成时，通知客户端
    """

    def __init__(self, *args, **kwargs):
        """
        初始化，定义组名
        """
        super().__init__(*args, **kwargs)
        self._group_name = ''

    async def connect(self):
        """
        处理连接，确定组名并添加组
        """
        job_uuid = self.scope['url_route']['kwargs']['uuid']
        self._group_name = f'job_{job_uuid}'

        await self.channel_layer.group_add(
            self._group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        """
        处理断开，删除组
        """
        await self.channel_layer.group_discard(
            self._group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        """
        处理从连接接收的信息
        """
        await self.close()

    async def chat_message(self, event):
        """
        处理从组接收的信息
        """
        await self.send(text_data=safe_json_dumps({
            'status': event['status'],
            'step': event['step'],
            'progress': event['progress']
        }))

        if event['progress'] == 1:
            await self.close()
