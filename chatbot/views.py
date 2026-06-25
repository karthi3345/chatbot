import os
import json
import logging

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from dotenv import load_dotenv
from mistralai.client import Mistral

from .prompts import SYSTEM_PROMPT

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


def home(request):
    return render(request, "chatbot/index.html")


@csrf_exempt
@require_POST
def chat(request):
    try:
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()
        
        if not user_message:
            return JsonResponse({"error": "Message is required"}, status=400)
        
        api_key = os.getenv("MISTRAL_API_KEY")
        
        if not api_key:
            logger.error("MISTRAL_API_KEY not found in .env")
            return JsonResponse({"error": "API key not configured"}, status=500)
        
        client = Mistral(api_key=api_key)
        
        response = client.chat.complete(
            model="mistral-large-latest",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )
        
        bot_reply = response.choices[0].message.content
        
        return JsonResponse({"reply": bot_reply})
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        logger.error(f"Error in chat view: {e}")
        return JsonResponse({"error": "Something went wrong"}, status=500)