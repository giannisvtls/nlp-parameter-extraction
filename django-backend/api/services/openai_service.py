from openai import AsyncOpenAI
from django.conf import settings
import json
from .rag_service import RAGService

SYSTEM_PROMPT = """You are a customer support agent of a Bank in Greece. Your role is to process user requests and extract relevant information.

Here is some relevant context that might help answer the user's question:
{context}

RESPONSE TYPES:
1. For banking operations, you MUST return a JSON response with the following schema:
{{
    "type": "banking_operation",
    "operation": {{
        "action": "One of: REGISTER, BALANCE, DEPOSIT, WITHDRAW, TRANSFER, IBAN",
        "user_name": "Name of the user (if provided)",
        "amount": "Numeric amount without currency (if provided)",
        "iban": "IBAN number (if provided for transfers)"
    }}
}}

2. For general inquiries or questions that can be answered using the context:
{{
    "type": "general_inquiry",
    "response": "Your informative response based on the context"
}}

BANKING OPERATIONS:
1. REGISTER: Create new user account
   Required: user_name
   Optional: amount (initial balance)

2. BALANCE: Check account balance and IBAN
   Required: user_name

3. WITHDRAW: Remove money from account
   Required: user_name, amount

4. DEPOSIT: Add money to account
   Required: user_name, amount

5. TRANSFER: Send money to another account
   Required: user_name, amount, iban

6. IBAN: Get IBAN information
   Required: user_name

RULES:
- Only include parameters in the JSON if they are present in the user's message
- For amounts, extract only the numeric value without currency symbols
- If the user's question is general and can be answered using the context, use the general_inquiry response type
- If unsure about the action type, use general_inquiry and provide a helpful response"""

class OpenAIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.rag_service = RAGService()

    async def process_message(self, message: str, message_history: list = None) -> dict:
        # Get relevant context from RAG service
        context = await self.rag_service.get_relevant_context(message)
        # Ensure context is a string, use empty string if None
        context = context if context is not None else ""
        try:
            # Initialize messages array
            messages = []
            
            # Add message history if provided, otherwise add system prompt
            if message_history:
                # Only add system prompt if it's not already in history
                if not any(msg.get('role') == 'system' for msg in message_history):
                    messages.append({"role": "system", "content": SYSTEM_PROMPT.format(context=context)})
                messages.extend(message_history)
            else:
                messages.append({"role": "system", "content": SYSTEM_PROMPT.format(context=context)})
            
            # Add current message
            messages.append({
                "role": "user",
                "content": message
            })
            
            try:
                response = await self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    temperature=0,
                    max_tokens=1500
                )
            except Exception as e:
                print(f"OpenAI API error: {str(e)}")
                return {
                    'status': 'error',
                    'error': f"OpenAI API error: {str(e)}",
                    'original_message': message
                }
            
            try:
                processed_response = response.choices[0].message.content
                # Parse the JSON response
                processed_response = json.loads(processed_response)
            except json.JSONDecodeError:
                # Log error without printing the context
                print("Failed to parse JSON response")
                processed_response = {"type": "general_inquiry", "response": "I apologize, but I couldn't process your request properly. Could you please rephrase it?"}
            except Exception as e:
                print(f"Error processing response: {str(e)}")
                return {
                    'status': 'error',
                    'error': f"Error processing response: {str(e)}",
                    'original_message': message
                }
            
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
