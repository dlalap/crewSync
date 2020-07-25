from channels.generic.websocket import AsyncWebsocketConsumer
import json
import random
from spotcontrol.spot import Spot


class SpotifyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'control_%s' % self.room_name
        # self.spot = Spot('test_username')
        # Join room group
        await self.channel_layer.group_add(
          self.room_group_name,
          self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
          self.room_group_name,
          self.channel_name
        )

    # Receive control message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        control = text_data_json['control']

        # Send control to room group
        await self.channel_layer.group_send(
          self.room_group_name,
          {
            'type': 'control_message',
            'control': control
          }
        )

        # if control == 'PLAY':
        #     self.spot.client.start_playback()

        # if control == 'PAUSE':
        #     self.spot.client.pause_playback()

    # Receive control message from room group
    async def control_message(self, event):
        control = event['control']

        # Send control message to WebSocket
        await self.send(text_data=json.dumps({
          'control': control
        }))