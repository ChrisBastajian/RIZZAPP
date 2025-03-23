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
    "friendly": "You are a friendly and helpful assistant, always cheerful and warm",
    "flirty": "You are a charming and flirtatious assistant, using playful and light-hearted language",
    "funny": "You are a funny assistant, telling jokes and making witty remarks",
    "confident": "You are a confident assistant, speaking with authority and certainty",
    "authoritative": "You are very authoritative and dominant in your transition. You are not easily pleased"
                    "with people trying to rizz you up"
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