from aiohttp import web
import openai
import jinja2
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

# Set up Jinja2 template rendering
template_loader = jinja2.FileSystemLoader("templates")
template_env = jinja2.Environment(loader=template_loader)

async def index(request):
    """Serve the HTML page."""
    template = template_env.get_template("index.html")
    return web.Response(text=template.render(), content_type="text/html")

async def chat(request):
    """Handle chat requests from frontend."""
    try:
        data = await request.json()
        user_message = data.get("message")

        # Call OpenAI API
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[{"role": "user", "content": user_message}]
        )

        bot_reply = response["choices"][0]["message"]["content"]
        return web.json_response({"response": bot_reply})

    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

# Create the aiohttp app and set routes
app = web.Application()
app.router.add_get("/", index)
app.router.add_post("/chat", chat)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=5000)  # Host on local network
