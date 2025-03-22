import os
import google.generativeai as genai
my_api_key = os.environ.get("GEMINI_API_KEY")
print(my_api_key)

def generate():
    genai.configure(api_key=my_api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")  # Ensure you use the correct model version
    response = model.generate_content("How is the weather today?")

    print(response.text)  # Proper way to access the response

if __name__ == "__main__":
    generate()
