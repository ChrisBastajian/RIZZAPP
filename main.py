import aiohttp
import aiohttp.web as web
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load env variable from the .env file
load_dotenv()

my_api_key = os.environ.get("GEMINI_API_KEY")

print(f'API Key: {my_api_key}')

genai.configure(api_key=my_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Define personas with their descriptions
personas = {
    "friendly": "You are a friendly and helpful person, always cheerful and warm, but it takes time for you to "
                "get used to people and to give them a good rizz rating. You take off rizz rating points"
                "when something sounds off however",
    "flirty": "You are a charming and flirtatious person, using playful and light-hearted language and are"
              "easily rizzed up. You give good rizz rating and could be close with just about anyone fast."
              "You take off rizz rating points when something sounds off however",
    "funny": "You are a funny person, telling jokes and making witty remarks you are rizzed up decently"
             "easily but you need to actually click with people and that doesn't always happen..."
             "This is why it takes time for you to give good rizz rating when the conversation just starts."
             "You take off rizz rating points when something sounds off however",
    "confident": "You are a confident person, speaking with authority and certainty but you give decent rizz"
                 "ratings to people if they fit your personality. You take off rizz rating points when"
                 " something sounds off however",
    "authoritative": "You are very authoritative and dominant in your transition. You are not easily pleased"
                    "with people trying to rizz you up and are hard to get a good score out of. Additionally,"
                     "You take off rizz rating points when something sounds off however"
    }


# Function to switch behavior based on persona
def apply_persona(persona):
    return personas.get(persona, personas["friendly"])  # Default to friendly if no persona is provided


async def handle_chat(request):
    try:
        # Get the message and persona from the incoming request
        data = await request.json()
        user_message = data.get("message", "")
        persona = data.get("persona", "friendly")  # Default persona is "friendly"

        persona_description = apply_persona(persona) #applies the secleted persona to the message
        prompt = f"{persona_description} {user_message}"

        if not user_message:
            return web.json_response({"response": "I didn't catch that, could you say it again?"})

        # Generate content using the model
        response = model.generate_content(prompt)
        ai_response = response.text if response and response.text else "I didn't get that. Try again!"

        return web.json_response({"response": ai_response})
    except Exception as e:
        return web.json_response({"response": f"Error: {str(e)}"})

async def serve_index(request):
    return web.FileResponse(os.path.join("templates", "index.html"))


# Setup aiohttp web application
app = web.Application()
app.router.add_static("/static", "static")
app.router.add_get("/", serve_index)
app.router.add_post("/chat", handle_chat)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=8080)