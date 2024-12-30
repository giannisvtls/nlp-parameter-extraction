from openai import AsyncOpenAI
from django.conf import settings
import json

SYSTEM_PROMPT = """You are a customer support agent of a Bank in Greece. Users will be asking to perform the following 5 actions: 1)User Registration by giving user name and optionally the initial account balance 2) Current Account balance, 3) Withdraw from balance, 4) Deposit to balance, 5) Transfer money to another account.
Select the best actions that fits what the bot asked and what the user responded to the question.
Rules to format your reply
You MUST format your reply in json using the following schema and if you don't find a value for a parameter don't return the parameter at all:
{
  "user_name": "extract any name you find in the user input",
  "action": "extract any action you see in the users message, this MUST be one of the following: "REGISTER", "BALANCE","DEPOSIT", "WITHDRAW", "TRANSFER" ",
  "iban": "extract any potential ibans to transfer money to",
  "amount": "extract any amount of money you see in the message, keep only the number not the currency"
}"""

class OpenAIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def process_message(self, message: str, message_history: list = None) -> dict:
        try:
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT}
            ]
            
            # Add message history if provided
            if message_history:
                messages.extend(message_history)
            
            # Add current message
            messages.append({
                "role": "user",
                "content": message
            })
            
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7,
                max_tokens=150
            )
            
            processed_response = response.choices[0].message.content
            
            # Parse the JSON response
            try:
                processed_response = json.loads(processed_response)
            except json.JSONDecodeError:
                processed_response = {"action": "UNKNOWN"}
            
            return {
                'status': 'success',
                'processed_message': processed_response,
                'original_message': message
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'original_message': message
            }