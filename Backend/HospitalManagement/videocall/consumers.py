from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
     rooms = {} 
     async def connect(self):
              self.roomid = self.scope['url_route']['kwargs']['roomid']
              self.room_group_name = f"Test-Room-{self.roomid}"
              if self.roomid in ChatConsumer.rooms:
                 if len(ChatConsumer.rooms[self.roomid]) >= 2:
                # Room is full, reject the connection
                  await self.close()
                  return
              else:
            # Create a new room
                  ChatConsumer.rooms[self.roomid] = []

        # Add the user to the room
              ChatConsumer.rooms[self.roomid].append(self.channel_name)

              await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
               )
             
              await self.accept()
     async def disconnect(self,close_code):
           if self.roomid in ChatConsumer.rooms:
              ChatConsumer.rooms[self.roomid].remove(self.channel_name)
              if not ChatConsumer.rooms[self.roomid]:
                 del ChatConsumer.rooms[self.roomid]
           await self.channel_layer.group_discard(
               self.room_group_name,
               self.channel_name
          )
           print('Disconnected')
     async def receive(self,text_data):
          recieve_dict=json.loads(text_data)
          print("incomming data is",recieve_dict)
          message=recieve_dict['message']
          action=recieve_dict['action']
          if(action=='new-offer') or (action=='new-answer'):
               receiver_channel_name=recieve_dict['message']['receive_channel_name']
               recieve_dict['message']['receive_channel_name']=self.channel_name
               await self.channel_layer.send(
                    receiver_channel_name,
                    {
                         'type':'send.sdp',
                         'receive_dict':recieve_dict
                    }
               )
               return 
          recieve_dict['message']['receive_channel_name']=self.channel_name
          await self.channel_layer.group_send(
               self.room_group_name,
               {
                'type':'send.sdp',
                'receive_dict':recieve_dict
               } 
          )
     async def send_sdp(self,event):
          receive_dict=event['receive_dict']
          await self.send(text_data=json.dumps(receive_dict))
