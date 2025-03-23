import aiohttp
import aiohttp.web as web
import os
import google.generativeai as genai

my_api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=my_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

async def handle_chat(request):
    try:
        data = await request.json()
        user_message = data.get("message", "")

        if not user_message:
            return web.json_response({"response": "I didn't catch that, could you say it again?"})

        response = model.generate_content(user_message)
        ai_response = response.text if response and response.text else "I didn't get that. Try again!"

        return web.json_response({"response": ai_response})
    except Exception as e:
        return web.json_response({"response": f"Error: {str(e)}"})

async def serve_index(request):
    return web.FileResponse(os.path.join("templates", "new_index.html"))


app = web.Application()
app.router.add_get("/", serve_index)
app.router.add_post("/chat", handle_chat)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=8080)
