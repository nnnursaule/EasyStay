from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes

from .models import Conversation, Message
import openai

class AIAssistantView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        user_message = request.data.get('message')
        conversation_id = request.data.get('conversation_id')
        
        if not user_message:
            return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get or create conversation
        if conversation_id:
            try:
                # Handle anonymous users
                if request.user.is_authenticated:
                    conversation = Conversation.objects.get(id=conversation_id, user=request.user)
                else:
                    conversation = Conversation.objects.get(id=conversation_id, user=None)
            except Conversation.DoesNotExist:
                return Response({"error": "Conversation not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Create new conversation (with or without a user)
            if request.user.is_authenticated:
                conversation = Conversation.objects.create(user=request.user)
            else:
                conversation = Conversation.objects.create(user=None)
        
        # Save user message
        Message.objects.create(
            conversation=conversation,
            role='user',
            content=user_message
        )
        
        # Get conversation history (limited to last 10 messages)
        messages = conversation.messages.all().order_by('timestamp')[:10]
        message_history = [{"role": msg.role, "content": msg.content} for msg in messages]
        
        # If no history, add system message
        if not message_history:
            message_history.append({
                "role": "system",
                "content": "You are EasyStay Assistant, a helpful AI that provides information about rental properties and accommodations. Be friendly and helpful."
            })
        
        # Add user's current message if it's not already in history
        if message_history[-1]["role"] != "user" or message_history[-1]["content"] != user_message:
            message_history.append({"role": "user", "content": user_message})
        
        try:
            # Call OpenAI API
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=message_history
            )
            
            assistant_response = response.choices[0].message.content
            
            # Save assistant response
            Message.objects.create(
                conversation=conversation,
                role='assistant',
                content=assistant_response
            )
            
            return Response({
                "response": assistant_response,
                "conversation_id": conversation.id
            })
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
