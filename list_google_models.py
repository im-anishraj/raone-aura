from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyAIFNdtRwPpM-wSEEbVhT9sXeYnJAF_0VY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

print("Fetching models from Google Gemini (via OpenAI Interface)...")

try:
    models = client.models.list()
    for model in models:
        print(f"Model ID: {model.id}")
except Exception as e:
    print(f"Error fetching models: {e}")
