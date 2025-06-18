from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render
from .models import Conversation, Message
from bookings.models import Apartment
import openai

import os
from dotenv import load_dotenv

openai.api_key = settings.OPENAI_API_KEY
class AIAssistantView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("API KEY ===>", os.environ.get("OPENAI_API_KEY"))
        user_message = request.data.get('message')
        conversation_id = request.data.get('conversation_id')

        if not user_message:
            return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Сначала создаём или получаем conversation
        if conversation_id:
            try:
                if request.user.is_authenticated:
                    conversation = Conversation.objects.get(id=conversation_id, user=request.user)
                else:
                    conversation = Conversation.objects.get(id=conversation_id, user=None)
            except Conversation.DoesNotExist:
                return Response({"error": "Conversation not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            conversation = Conversation.objects.create(user=request.user if request.user.is_authenticated else None)

        # Save user message
        Message.objects.create(
            conversation=conversation,
            role='user',
            content=user_message
        )

        # Обработка запроса "все квартиры"
        if "all apartments" in user_message.lower() or "все квартиры" in user_message.lower():
            apartments = Apartment.objects.filter(status="available")[:10]
            if apartments.exists():
                apt_list = []
                for apt in apartments:
                    price = f"{apt.price_per_month} KZT/month" if apt.rental_type == 'month' else f"{apt.price_per_day} KZT/day"
                    apt_list.append(f"{apt.title} — {price}, {apt.rooms} rooms")
                return Response({
                    "response": "Here are some available apartments:\n\n" + "\n".join(apt_list),
                    "conversation_id": conversation.id
                })
            else:
                return Response({
                    "response": "No available apartments found.",
                    "conversation_id": conversation.id
                })
        if not user_message:
            return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Get or create conversation
        if conversation_id:
            try:
                if request.user.is_authenticated:
                    conversation = Conversation.objects.get(id=conversation_id, user=request.user)
                else:
                    conversation = Conversation.objects.get(id=conversation_id, user=None)
            except Conversation.DoesNotExist:
                return Response({"error": "Conversation not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            conversation = Conversation.objects.create(user=request.user if request.user.is_authenticated else None)

        # Save user message
        Message.objects.create(
            conversation=conversation,
            role='user',
            content=user_message
        )

        # 🔍 Обработка запроса по квартирам до обращения к OpenAI
        region_keywords = {
            "alatau": "alatau",
            "алатау": "alatau",
            "бостандык": "bostandyk",
            "auyezov": "auyezov",
            "ауэзов": "auyezov",
            "медеу": "medeu",
            "наурызбай": "nauryzbay",
            "almaly": "almaly",
            "алмалы": "almaly",
            "турксиб": "turksib",
            "жетысу": "zhetysu",
        }

        matched_region_code = None
        for keyword, code in region_keywords.items():
            if keyword.lower() in user_message.lower():
                matched_region_code = code
                break

        if matched_region_code:
            apartments = Apartment.objects.filter(region=matched_region_code, status='available')[:5]
            if apartments.exists():
                apt_list = []
                for apt in apartments:
                    price = f"{apt.price_per_month} KZT/month" if apt.rental_type == 'month' else f"{apt.price_per_day} KZT/day"
                    apt_list.append(f"{apt.title} — {price}, {apt.rooms} rooms")

                return Response({
                    "response": f"Here are some apartments in {matched_region_code.capitalize()}:\n\n" + "\n".join(apt_list),
                    "conversation_id": conversation.id
                })
            else:
                return Response({
                    "response": f"No apartments found in {matched_region_code.capitalize()} region.",
                    "conversation_id": conversation.id
                })

        # Получение истории сообщений
        messages = conversation.messages.all().order_by('timestamp')[:10]
        message_history = [{"role": msg.role, "content": msg.content} for msg in messages]

        if not message_history:
            message_history.append({
                "role": "system",
                "content": "You are EasyStay Assistant, a helpful AI that provides information about rental properties and accommodations. Be friendly and helpful."
            })

        if message_history[-1]["role"] != "user" or message_history[-1]["content"] != user_message:
            message_history.append({"role": "user", "content": user_message})

        try:
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=message_history
            )

            assistant_response = response.choices[0].message.content

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
            print(str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def ai_assistant_template(request):
    return render(request, 'ai_assistant.html')
