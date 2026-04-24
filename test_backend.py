import asyncio
from aura.core.llm.backend.openai import OpenAIBackend
from aura.core.types import LLMMessage, Role, LLMChunk, LLMUsage, ModelConfig, ProviderConfig, Backend, AvailableTool

async def main():
    print("Testing OpenAIBackend...")
    
    # Mock Config
    provider = ProviderConfig(
        name="openai",
        api_base="https://api.groq.com/openai/v1",
        api_key_env_var="GROQ_API_KEY", # or whatever, logic handles hardcode
        backend=Backend.OPENAI
    )
    
    backend = OpenAIBackend(provider)
    
    # Test Message
    messages = [
        LLMMessage(role=Role.user, content="Who are you?")
    ]
    
    # Model Config
    model = ModelConfig(
        name="llama-3.3-70b-versatile",
        provider="openai",
        alias="terminal-mind"
    )

    try:
        print("Calling complete()...")
        response = await backend.complete(
            model=model,
            messages=messages,
            temperature=0.7,
            tools=[],
            max_tokens=1000,
            tool_choice=None,
            extra_headers={}
        )
        print("Response received!")
        print(f"Content: {response.message.content}")
        print(f"Usage: {response.usage}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
