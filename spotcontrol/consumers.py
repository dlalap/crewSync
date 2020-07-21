from channels.generic.websocket import AsyncWebsocketConsumer
from spotcontrol.models import SpotifyUser
# from asgiref.sync import sync_to_async
import json
import random
import spotcontrol.spotcontroller as sc
import datetime as dt
# from spotcontrol.spot import Spot


class SpotifyConsumer(AsyncWebsocketConsumer):

    def __init__(self):
        print("Initializing SpotifyConsumer class.")

    async def connect(self):
        print(f'SpotifyConsumer.scope = {self.scope}')
        self.crew_id = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'control_%s' % self.crew_id
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
        # targetTime = text_data_json['targetTime']
        targetTime = text_data_json.get('targetTime', None)
        print(f'targetTime: {targetTime}')

        print(f'control to send: {control}')
        # auth_token = sync_to_async(self.TryGetAuthToken())
        auth_token = self.TryGetAuthToken()

        control_package = {
            'type': 'control_message',
            'control': control,
            'auth_token': auth_token,
            'targetTime': targetTime
          }          

        # Send control to room group
        await self.channel_layer.group_send(
          self.room_group_name,
          control_package
        )
        # spotUserValid = SpotifyUser.objects.get(username=self.user.id)
        # response = sc.sendSpotControl(control, auth_token)
        # print(response.text)

    # Receive control message from room group
    async def control_message(self, event):
        control = event['control']
        targetTime = event['targetTime']

        control_package = {
            'control': control,
            # 'auth_token': sync_to_async(self.TryGetAuthToken()),
            'auth_token': self.TryGetAuthToken(),
            'targetTime': targetTime,
            # 'most_recent_device': sync_to_async(self.TryGetLastDeviceUsed())
            'most_recent_device': self.TryGetLastDeviceUsed()
        }
        # Send control message to WebSocket
        await self.send(text_data=json.dumps(
            control_package
        ))

    def TryGetAuthToken(self):
        print('TryGetAuthToken() initiated')
        self.user = self.scope['user']
        spotUsersAvail = SpotifyUser.objects.filter(username=self.user)
        if spotUsersAvail == 0:
            return None
        else:
            return spotUsersAvail[0].auth_token

    def TryGetLastDeviceUsed(self):
        print('TryGetLastDeviceUsed() initiated')
        self.user = self.scope['user']
        spotUsersAvail = SpotifyUser.objects.filter(username=self.user)
        if spotUsersAvail == 0:
            return None
        else:
            return spotUsersAvail[0].most_recent_device