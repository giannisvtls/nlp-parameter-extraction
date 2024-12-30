from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
from api.services.user_service import UserService
from .services.openai_service import OpenAIService

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Attempting to connect...")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.openai_service = OpenAIService()
        self.user_service = UserService()

        # Initialize message history
        self.message_history = []
        
        print(f"Room name: {self.room_name}")
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print("Group added, accepting connection...")
        await self.accept()
        
        # Store and send initial bot message
        initial_message = 'Register by typing your full name and your current account balance'
        self.message_history.append({
            'role': 'assistant',
            'content': initial_message
        })
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': initial_message,
                'username': 'Bot'
            }
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json.get('username', 'Anonymous')
        
        # Add user message to history
        self.message_history.append({
            'role': 'user',
            'content': message
        })
        
        # Process the incoming message with history
        processed_result = await self.openai_service.process_message(message, self.message_history)
        
        # Send the original message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

        if processed_result['status'] == 'success':
            processed_message = processed_result['processed_message']
            bot_response = "I couldn't process that request"
           
            if processed_message.get('action') == 'REGISTER' and processed_message.get('user_name'):
                user_service = UserService()
                user, message = await self.user_service.create_user(
                    name=processed_message.get('user_name'),
                    initial_balance=processed_message.get('amount', 0)
                )
               
                if user:
                    bot_response = f"Successfully registered user {user.name} with IBAN: {user.iban} and initial balance: {user.balance}"
                else:
                    bot_response = f"Failed to register user: {message}"

            # Add bot response to history
            self.message_history.append({
                'role': 'assistant',
                'content': bot_response
            })
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': bot_response,
                    'username': 'Bot'
                }
            )
        else:
            error_message = f"Error processing request: {processed_result['error']}"
            # Add error message to history
            self.message_history.append({
                'role': 'assistant',
                'content': error_message
            })
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': error_message,
                    'username': 'Bot'
                }
            )

    async def disconnect(self, close_code):
        # Simply clean up the group connection when disconnecting
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))