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
from .mojoslc_prompts import MOJOSLC_PROMPT
from .evolution_prompts import EVOLUTION_PROMPT

load_dotenv()

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_FILE = os.path.join(BASE_DIR, "chatbot", "data", "7mojos.json")

# Load games and convert dict to list of game objects
with open(JSON_FILE, "r", encoding="utf-8") as f:
    GAMES = list(json.load(f).values())

print("=" * 50)
print(f"✅ SERVER STARTED - Loaded {len(GAMES)} 7Mojos Games")
for g in GAMES:
    print(f"   -> {g['game_name']}")
print("=" * 50)


def find_game(query: str) -> dict | None:
    """Search for a game by name (case-insensitive partial match)."""
    query_lower = query.strip().lower()
    
    for game in GAMES:
        if query_lower in game["game_name"].lower():
            return game
    return None


def format_game_reply(game: dict) -> str:
    """Format a game dict into the required response format."""
    unique = "\n".join(
        [f"• {item}" for item in game.get("what_makes_it_unique", [])]
    )
    
    return f"""**Game Name:** {game['game_name']}

**Description:**
{game['description']}

**What Makes It Unique:**
{unique}"""


def home(request):
    return render(request, "chatbot/index.html")


@csrf_exempt
@require_POST
def chat(request):
    try:
        data = json.loads(request.body)

        user_message = data.get("message", "").strip()
        # Default to general if frontend doesn't send it (like your current HTML)
        assistant = data.get("assistant", "general").lower()

        print(f"\n📩 Incoming message: '{user_message}' (Assistant selected: '{assistant}')")

        if not user_message:
            return JsonResponse({"error": "Message is required"}, status=400)

        # ============================================
        # MANDATORY CHECK: 7Mojos Games Database
        # This runs for EVERY message to prevent AI hallucinations
        # ============================================
        game = find_game(user_message)
        
        if game:
            print(f"🛑 AI BLOCKED: Found '{game['game_name']}' in JSON. Returning exact data.")
            reply = format_game_reply(game)
            return JsonResponse({"reply": reply})

        # ============================================
        # FALLBACK: Call Mistral AI (Only if NO game was found)
        # ============================================
        print(f"🤖 No game found in JSON. Calling Mistral AI...")
        
        api_key = os.getenv("MISTRAL_API_KEY")

        if not api_key:
            return JsonResponse(
                {"error": "MISTRAL_API_KEY not configured"},
                status=500
            )

        # Select the correct system prompt based on assistant type
        if assistant == "7mojos":
            system_prompt = MOJOSLC_PROMPT
        elif assistant == "evolution":
            system_prompt = EVOLUTION_PROMPT
        else:
            system_prompt = SYSTEM_PROMPT

        client = Mistral(api_key=api_key)

        response = client.chat.complete(
            model="mistral-large-latest",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_message,
                },
            ],
        )

        bot_reply = response.choices[0].message.content
        print(f"✅ AI Response received.")

        return JsonResponse({"reply": bot_reply})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    except Exception as e:
        logger.exception(e)
        return JsonResponse({"error": "Something went wrong"}, status=500)
    
    
from difflib import get_close_matches

def find_game(query: str) -> dict | None:
    """Search for a game by name with typo tolerance."""
    query_lower = query.strip().lower()
    
    # 1. Try exact substring match first
    for game in GAMES:
        if query_lower in game["game_name"].lower():
            return game
            
    # 2. If no exact match, try fuzzy matching to catch typos (like "Rouletter")
    game_names = {game["game_name"].lower(): game for game in GAMES}
    matches = get_close_matches(query_lower, game_names.keys(), n=1, cutoff=0.8)
    
    if matches:
        return game_names[matches[0]]
        
    return None