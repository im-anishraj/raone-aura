import sys
import os

# Ensure we can import from the 'mistral-vibe' directory if we are running from root
sys.path.append(os.path.join(os.getcwd(), 'mistral-vibe'))

try:
    from vibe.core.config import VibeConfig
except ImportError:
    # If the above fails, try assuming we are inside mistral-vibe wrapper
    sys.path.append(os.getcwd())
    from vibe.core.config import VibeConfig

def main():
    print("Loading VibeConfig...")
    try:
        config = VibeConfig.load()
    except Exception as e:
        print(f"Error loading config: {e}")
        return

    print(f"\nActive Model: {config.active_model}")
    
    active_model_config = config.get_active_model()
    print(f"Active Model Config Provider: {active_model_config.provider}")
    
    active_provider = config.get_provider_for_model(active_model_config)
    print(f"\nActive Provider: {active_provider.name}")
    print(f"Provider API Base: {active_provider.api_base}")
    print(f"Provider Backend: {active_provider.backend}")
    print(f"Provider Environment Variable for Key: {active_provider.api_key_env_var}")
    
    key_val = os.getenv(active_provider.api_key_env_var)
    if key_val:
        print(f"API Key Found: Yes (Length: {len(key_val)})")
    else:
        print("API Key Found: NO")

if __name__ == "__main__":
    main()
