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
from .pgsoft_prompts import prompts

load_dotenv()
logger = logging.getLogger(__name__)

# =====================================================
# PATH CONFIGURATION
# =====================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOJOS_FILE = os.path.join(BASE_DIR, "chatbot", "data", "7mojos.json")
EVOLUTION_FILE = os.path.join(BASE_DIR, "chatbot", "data", "evolution.json")
BETONGAMES_FILE = os.path.join(BASE_DIR, "chatbot", "data", "betongames.json")
JACKTOP_FILE = os.path.join(BASE_DIR, "chatbot", "data", "jacktop.json")
PGSOFT_FILE = os.path.join(BASE_DIR, "chatbot", "data", "pgsoft.json")
BGAMES_FILE=os.path.join (BASE_DIR,"chatbot","data","bgames.json")
BETGAMES_FILE=os.path.join(BASE_DIR,"chatbot","data","betgames.json")
WINMATCH_FILE=os.path.join(BASE_DIR,"chatbot","data","winmatch.json")
ELCASINO_FILE=os.path.join(BASE_DIR,"chatbot","data","elcasino.json")
TVBET_FILE=os.path.join(BASE_DIR,"chatbot","data","tvbet.json")
KAGAMING_FILE=os.path.join(BASE_DIR,"chatbot","data","kagaming.json")
SPRIBE_FILE=os.path.join(BASE_DIR,"chatbot","data","spribe.json")
AVIATRIX_FILE=os.path.join(BASE_DIR,"chatbot","data","aviatrix.json")
PIGABOOM_FILE=os.path.join(BASE_DIR,"chatbot","data","pigaboom.json")
SPIN4WIN_FILE=os.path.join(BASE_DIR,"chatbot","data","1spin4win.json")
TURBO_FILE=os.path.join(BASE_DIR,"chatbot","data","turbogame.json")
SMARTSOFT_FILE=os.path.join(BASE_DIR,"chatbot","data","smartsof.json")
BGAMING_FILE=os.path.join(BASE_DIR,"chatbot","data","bgaming.json")
# =====================================================
# LOAD JSON DATABASES
# =====================================================
def load_json(filepath, label):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return list(json.load(f).values())
    except FileNotFoundError:
        print(f"⚠️ {label} not found!")
        return []

MOJOS_GAMES = load_json(MOJOS_FILE, "7mojos.json")
EVOLUTION_GAMES = load_json(EVOLUTION_FILE, "evolution.json")
BETONGAMES_GAMES = load_json(BETONGAMES_FILE, "betongames.json")
JACKTOP_GAMES = load_json(JACKTOP_FILE, "jacktop.json")
PGSOFT_GAMES = load_json(PGSOFT_FILE, "pgsoft.json")
BGAMES_GAMES=load_json(BGAMES_FILE,"bgames.json")
BETGAMES_GAMES=load_json(BETGAMES_FILE,"betgames.json")
WINMATCH_GAMES=load_json(WINMATCH_FILE,"winmatch.json")
ELCASINO_GAMES=load_json(ELCASINO_FILE,"elcasino.json")
TVBET_GAMES=load_json(TVBET_FILE,"tvbet.json")
KAGAMING_GAMES=load_json(KAGAMING_FILE,"kagaming.json")
SPRIBE_GAMES=load_json(SPRIBE_FILE,"spribe.json")
AVIATRIX_GAMES=load_json(AVIATRIX_FILE,"aviatrix.json")
PIGABOOM_GAMES=load_json(PIGABOOM_FILE,"pigaboom.json")
SPIN4WIN_GAMES=load_json(SPRIBE_FILE,"1spin4win.json")
TURBO_GAMES=load_json(TURBO_FILE,"turbogame.json")
SMARTSOFT_GAMES=load_json(SMARTSOFT_FILE,"smartsof.json")
BGAMING_GAMES=load_json(BGAMING_FILE,"bgames.json")

ALL_GAMES = MOJOS_GAMES + EVOLUTION_GAMES + BETONGAMES_GAMES + JACKTOP_GAMES + PGSOFT_GAMES + BGAMES_GAMES+BETGAMES_GAMES+WINMATCH_GAMES+ELCASINO_GAMES+TVBET_GAMES+KAGAMING_GAMES+SPRIBE_GAMES+AVIATRIX_GAMES+PIGABOOM_GAMES+SPIN4WIN_GAMES+SMARTSOFT_GAMES+TURBO_GAMES+BGAMING_GAMES

print("=" * 60)
print("✅ GAME DATABASE LOADED")
print(f"7MOJOS GAMES : {len(MOJOS_GAMES)}")
print(f"EVOLUTION GAMES : {len(EVOLUTION_GAMES)}")
print(f"BETONGAMES GAMES : {len(BETONGAMES_GAMES)}")
print(f"JACKTOP GAMES : {len(JACKTOP_GAMES)}")
print(f"PGSOFT GAMES : {len(PGSOFT_GAMES)}")
print(f"BGAMES : {len(BGAMES_GAMES)}")
print(f"BETGAMES : {len(BETGAMES_GAMES)}")
print(f"WINMATCHGAMES : {len(WINMATCH_GAMES)}")
print(f"ELCASINOGAMES: {len(ELCASINO_GAMES)}")
print(f"TVBETGAMES: {len(TVBET_GAMES)}")
print(f"KAGAMING: {len(KAGAMING_GAMES)}")
print(f"SPRIBE: {len(SPRIBE_GAMES)}")
print(f"AVIATRIX: {len(AVIATRIX_GAMES)}")
print(f"PIGABOOM: {len(PIGABOOM_GAMES)}")
print(f"1SPIN4WIN: {len(SPIN4WIN_GAMES)}")
print(f"SMARTSOFT: {len(SMARTSOFT_GAMES)}")
print(f"TURBOGAMES: {len(TURBO_GAMES)}")
print(f"BGAMING: {len(BGAMING_GAMES)}")
print(f"TOTAL (with duplicates) : {len(ALL_GAMES)}")

print("=" * 60)

# =====================================================
# EXACT MATCH ONLY
# =====================================================
import re

def normalize_name(text):
    return re.sub(r'[^a-z0-9]', '', str(text).lower())

def find_game_exact(query, games):
    """
    Returns exactly ONE game or NONE.
    Ignores spaces, hyphens and case.
    """

    search_name = normalize_name(query)

    for game in games:

        game_name = normalize_name(
            game.get("game_name", "")
        )

        if game_name == search_name:
            return game

    return None

# =====================================================
# FORMAT GAME RESPONSE
# =====================================================
def format_game_reply(game):
    unique = "\n".join([f"• {item}" for item in game.get("what_makes_it_unique", [])])
    return f"""**{game.get('game_name')}**

{game.get('description', '')}

**What Makes It Unique:**
{unique}"""

# =====================================================
# HOME PAGE
# =====================================================
def home(request):
    return render(request, "chatbot/index.html")

# =====================================================
# CHAT API
# =====================================================
@csrf_exempt
@require_POST
def chat(request):
    try:
        data = json.loads(request.body)

        user_message = data.get("message", "").strip()
        assistant = data.get("assistant", "general").lower()

        print(f"\n📩 Message : {user_message}")

        if not user_message:
            return JsonResponse(
                {"error": "Message required"},
                status=400
            )

        query = user_message.lower()


        # ==========================================
        # PROVIDER DETECT
        # ==========================================
        def detect_provider(query):

            providers = [
                "winmatch",
                "pigboom",
                "pgsoft",
                "evolution",
                "7mojos",
                "pragmatic",
                "hacksaw",
                "pigaboom",
                "tvbet",
                
            ]

            for provider in providers:
                if provider in query:
                    return provider

            return None

        query = user_message.lower()
        print("QUERY =", query)
        if (
    " vs " in query or
    " and " in query or "compare" in query):
         return cmp_2_games(request)
         


        # ==========================================
        # HIGHEST RTP GAMES
        # ==========================================
        if (
            "highest rtp" in query or
            "high rtp" in query or
            "best rtp" in query or
            "top rtp" in query
        ):

            provider = detect_provider(query)

            rtp_games = []


            for game in ALL_GAMES:

                # Provider Filter
                if provider:

                    game_provider = str(
                        game.get("provider", "")
                    ).lower()

                    if game_provider != provider:
                        continue


                rtp = game.get("rtp")

                if rtp:

                    try:

                        value = float(
                            str(rtp)
                            .replace("%", "")
                            .strip()
                        )

                        rtp_games.append(
                            (value, game)
                        )

                    except:
                        pass



            if rtp_games:

                highest_game = max(
                    rtp_games,
                    key=lambda x: x[0]
                )[1]


                return JsonResponse({

                    "reply":
                    f"🎰 Highest RTP Game\n\n"
                    f"• {highest_game['game_name']} "
                    f"— RTP: {highest_game['rtp']}"

                })


            return JsonResponse({

                "reply":
                "No RTP games found."

            })




        # ==========================================
        # LOWEST RTP GAMES
        # ==========================================
        if (
            "lowest rtp" in query or
            "low rtp" in query or
            "worst rtp" in query
        ):


            provider = detect_provider(query)

            rtp_games = []


            for game in ALL_GAMES:


                if provider:

                    game_provider = str(
                        game.get("provider","")
                    ).lower()


                    if game_provider != provider:
                        continue



                rtp = game.get("rtp")


                if rtp:

                    try:

                        value = float(
                            str(rtp)
                            .replace("%","")
                            .strip()
                        )


                        rtp_games.append(
                            (value,game)
                        )


                    except:
                        pass



            if rtp_games:


                lowest_game = min(
                    rtp_games,
                    key=lambda x:x[0]
                )[1]


                return JsonResponse({

                    "reply":
                    f"🎰 Lowest RTP Game\n\n"
                    f"• {lowest_game['game_name']} "
                    f"— RTP: {lowest_game['rtp']}"

                })



            return JsonResponse({

                "reply":
                "No RTP games found."

            })




        # ==========================================
        # RTP LOOKUP SPECIFIC GAME
        # ==========================================
        if "rtp" in query:


            sorted_games = sorted(
                ALL_GAMES,
                key=lambda g:
                len(
                    g.get("game_name","")
                ),
                reverse=True
            )


            for game in sorted_games:


                game_name = (
                    game.get(
                        "game_name",
                        ""
                    )
                    .lower()
                    .strip()
                )


                if (
                    game_name and
                    game_name in query
                ):


                    rtp = game.get("rtp")


                    if rtp:

                        return JsonResponse({

                            "reply":
                            f"🎰 {game['game_name']}\n\n"
                            f"RTP: {rtp}"

                        })



                    return JsonResponse({

                        "reply":
                        f"🎰 {game['game_name']}\n\n"
                        "RTP information unavailable."

                    })





        # ==========================================
        # EXACT GAME MATCH
        # ==========================================
        matched_game = find_game_exact(
            user_message,
            ALL_GAMES
        )


        if matched_game:


            print(
                f"✅ JSON MATCH : "
                f"{matched_game['game_name']}"
            )


            return JsonResponse({

                "reply":
                format_game_reply(
                    matched_game
                )

            })





        # ==========================================
        # MISTRAL FALLBACK
        # ==========================================
        print("🤖 Calling Mistral...")


        api_key = os.getenv(
            "MISTRAL_API_KEY"
        )


        if not api_key:

            return JsonResponse({

                "error":
                "MISTRAL_API_KEY missing"

            }, status=500)



        if assistant == "7mojos":

            system_prompt = MOJOSLC_PROMPT


        elif assistant == "evolution":

            system_prompt = EVOLUTION_PROMPT


        elif assistant == "pgsoft":

            system_prompt = prompts


        else:

            system_prompt = SYSTEM_PROMPT





        client = Mistral(
            api_key=api_key
        )


        response = client.chat.complete(

            model="mistral-large-latest",

            temperature=0,

            messages=[

                {
                    "role":"system",
                    "content":system_prompt
                },

                {
                    "role":"user",
                    "content":user_message
                }

            ]

        )



        return JsonResponse({

            "reply":
            response
            .choices[0]
            .message
            .content

        })




    except json.JSONDecodeError:


        return JsonResponse({

            "error":
            "Invalid JSON"

        }, status=400)




    except Exception as e:


        logger.exception(e)


        return JsonResponse({

            "error":
            "Something went wrong"

        }, status=500)
        
        

        
@csrf_exempt
@require_POST
def cmp_2_games(request):
    try:
        data = json.loads(request.body)

        query = data.get("message", "").strip().lower()

        print("🔥 COMPARE FUNCTION HIT")
        print("QUERY:", query)

        # Support both:
        # compare game1 vs game2
        # compare game1 and game2

        if " vs " in query:
            parts = query.replace("compare", "", 1).split(" vs ")

        elif " and " in query:
            parts = query.replace("compare", "", 1).split(" and ")

        else:
            return JsonResponse({
                "reply": "Use: compare Game1 vs Game2"
            })

        if len(parts) != 2:
            return JsonResponse({
                "reply": "Invalid comparison format."
            })

        game1_name = parts[0].strip()
        game2_name = parts[1].strip()

        print("GAME1:", game1_name)
        print("GAME2:", game2_name)

        game1 = find_game_exact(game1_name, ALL_GAMES)
        game2 = find_game_exact(game2_name, ALL_GAMES)

        print("FOUND GAME1:", game1)
        print("FOUND GAME2:", game2)

        if not game1:
            return JsonResponse({
                "reply": f"Game not found: {game1_name}"
            })

        if not game2:
            return JsonResponse({
                "reply": f"Game not found: {game2_name}"
            })

        # Description
        description1 = (
            game1.get("description")
            or game1.get("Description")
            or game1.get("game_description")
            or "N/A"
        )

        description2 = (
            game2.get("description")
            or game2.get("Description")
            or game2.get("game_description")
            or "N/A"
        )

        # Unique Feature
        unique1 = (
            game1.get("what_makes_it_unique")
            or game1.get("What Makes It Unique")
            or game1.get("unique")
            or game1.get("uniqueness")
            or "N/A"
        )

        unique2 = (
            game2.get("what_makes_it_unique")
            or game2.get("What Makes It Unique")
            or game2.get("unique")
            or game2.get("uniqueness")
            or "N/A"
        )

        # Convert list -> string
        if isinstance(unique1, list):
            unique1 = " ".join(str(x) for x in unique1)

        if isinstance(unique2, list):
            unique2 = " ".join(str(x) for x in unique2)

        table_html = f"""
        <h3>🎮 Game Comparison</h3>

        <table border="1" cellpadding="8" cellspacing="0"
               style="border-collapse:collapse;width:100%;">

            <tr>
                <th>Feature</th>
                <th>{game1.get('game_name', '')}</th>
                <th>{game2.get('game_name', '')}</th>
            </tr>

            <tr>
                <td>Description</td>
                <td>{description1}</td>
                <td>{description2}</td>
            </tr>

            <tr>
                <td>What Makes It Unique</td>
                <td>{unique1}</td>
                <td>{unique2}</td>
            </tr>

        </table>
        """

        print("✅ COMPARISON GENERATED")

        return JsonResponse({
            "reply": table_html 
        })

    except Exception as e:
        logger.exception(e)

        return JsonResponse({
            "reply": f"Error: {str(e)}"
        }, status=500)