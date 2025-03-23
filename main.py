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

# Handle the user's message and generate a response
async def handle_chat(request):
    try:
        data = await request.json()
        user_message = data.get("message", "")
        persona = data.get("persona", "friendly")  # Default persona is "friendly"

        if not user_message:
            return web.json_response({"response": "I didn't catch that, could you say it again?", "rating": None})

        persona_description = apply_persona(persona)
        prompt = f"{persona_description} {user_message}"

        # Generate AI response
        response = model.generate_content(prompt)
        ai_response = response.text if response and response.text else "I didn't get that. Try again!"

        return web.json_response({"response": ai_response, "rating": None})  # Send response first

    except Exception as e:
        return web.json_response({"response": f"Error: {str(e)}", "rating": None})


# Rate the rizz level of the message
async def rate_rizz(request):
    try:
        data = await request.json()
        user_message = data.get("message", "")

        if not user_message:
            return web.json_response({"rating": 0})

        # Ask AI to rate the rizz level
        rating_prompt = f"On a scale of 0 to 100, how much rizz does the following message have? Just return a number. Message: '{user_message}'"
        rating_response = model.generate_content(rating_prompt)

        try:
            rizz_rating = int(rating_response.text.strip())  # Extract and convert rating
            rizz_rating = max(0, min(100, rizz_rating))  # Ensure it's between 0-100
        except:
            rizz_rating = 50  # Default rating in case AI fails

        return web.json_response({"rating": rizz_rating})  # Send rating separately

    except Exception as e:
        return web.json_response({"rating": 0})


# Setup aiohttp web application
app = web.Application()
app.router.add_static("/static", "static")
app.router.add_get("/", lambda request: web.FileResponse(os.path.join("templates", "index.html")))
app.router.add_post("/chat", handle_chat)  # Route for handling chat messages
app.router.add_post("/rate", rate_rizz)  # Route for rating the rizz level

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=8080)
