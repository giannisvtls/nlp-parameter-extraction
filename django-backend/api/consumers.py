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

        # Initialize message history and user context
        self.message_history = []
        self.current_user = None  # Store current user's name
        self.current_iban = None  # Store current user's IBAN
        
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
        
        # Process the incoming message with history by calling OpenAI
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

        # Process only if the Request to OPEN AI was a success
        if processed_result['status'] == 'success':
            processed_message = processed_result['processed_message']
            bot_response = "I couldn't process that request"

            # Handle different response types
            if processed_message.get('type') == 'banking_operation':
                operation = processed_message.get('operation', {})
                action = operation.get('action')
                
                # HANDLE REGISTRATION
                if action == 'REGISTER' and operation.get('user_name'):
                    user_service = UserService()
                    user, message = await self.user_service.create_user(
                        name=operation.get('user_name'),
                        initial_balance=operation.get('amount', 0)
                    )
                
                    if user:
                        # Store user context after successful registration
                        self.current_user = user.name
                        self.current_iban = user.iban
                        bot_response = f"Successfully registered user {user.name} with IBAN: {user.iban} and initial balance: {user.balance}"
                    else:
                        bot_response = f"Failed to register user: {message}"

                # Handle balance check
                elif action == 'BALANCE':
                    if self.current_user:
                        try:
                            user = await self.user_service.get_user_by_name(self.current_user)
                            if user:
                                bot_response = f"Current balance for {user.name}: {user.balance} euros\nYour IBAN: {user.iban}"
                            else:
                                bot_response = "Could not find your account. Please register first."
                        except Exception as e:
                            bot_response = f"Error retrieving balance: {str(e)}"
                    else:
                        bot_response = "Please register first before checking balance."

                # Handle IBAN check
                elif action == 'IBAN':
                    if self.current_user:
                        try:
                            user = await self.user_service.get_user_by_name(self.current_user)
                            if user:
                                bot_response = f"Your IBAN is: {user.iban}"
                            else:
                                bot_response = "Could not find your account. Please register first."
                        except Exception as e:
                            bot_response = f"Error retrieving IBAN: {str(e)}"
                    else:
                        bot_response = "Please register first before checking your IBAN."

                # Handle withdrawal
                elif action == 'WITHDRAW':
                    if self.current_user and operation.get('amount'):
                        success, message = await self.user_service.withdraw(
                            self.current_user,
                            operation.get('amount')
                        )
                        bot_response = message
                    else:
                        bot_response = "Please register first and specify an amount to withdraw."

                # Handle deposit
                elif action == 'DEPOSIT':
                    if self.current_user and operation.get('amount'):
                        success, message = await self.user_service.deposit(
                            self.current_user,
                            operation.get('amount')
                        )
                        bot_response = message
                    else:
                        bot_response = "Please register first and specify an amount to deposit."

                # Handle transfer
                elif action == 'TRANSFER':
                    if self.current_user and operation.get('amount') and operation.get('iban'):
                        try:
                            user = await self.user_service.get_user_by_name(self.current_user)
                            if user:
                                success, message = await self.user_service.transfer_money(
                                    user,
                                    operation.get('amount'),
                                    operation.get('iban')
                                )
                                bot_response = message
                            else:
                                bot_response = "Could not find your account. Please register first."
                        except Exception as e:
                            bot_response = f"Error processing transfer: {str(e)}"
                    else:
                        bot_response = "Please register first and provide transfer amount and recipient IBAN."

            # Handle general inquiries
            elif processed_message.get('type') == 'general_inquiry':
                bot_response = processed_message.get('response', "I couldn't process that request")

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
