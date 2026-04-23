import asyncio
import os
from openai import AsyncOpenAI

from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("Error: OPENAI_API_KEY not found in .env")
    exit(1)

async def main():
    print("Testing connection to GitHub Models (Azure Inference)...")
    
    client = AsyncOpenAI(
        api_key=api_key,
        base_url="https://models.inference.ai.azure.com",
    )

    try:
        response = await client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Hello, are you working?",
                }
            ],
            model="gpt-4o",
            temperature=1.0,
            max_tokens=1000,
            top_p=1.0
        )

        print("\nSuccess! Response:")
        print(response.choices[0].message.content)

    except Exception as e:
        print("\nFailed to connect/generate:")
        print(e)

if __name__ == "__main__":
    asyncio.run(main())
