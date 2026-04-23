import os
import sys
from dotenv import load_dotenv

def main():
    print(f"Current Working Directory: {os.getcwd()}")
    
    # Attempt to load .env
    loaded = load_dotenv()
    print(f".env loaded: {loaded}")

    key = os.getenv("OPENAI_API_KEY")
    
    if not key:
        print("OPENAI_API_KEY not found in environment.")
        return

    print(f"Key Length: {len(key)}")
    
    if len(key) > 8:
        print(f"Key Preview: {key[:4]}...{key[-4:]}")
    else:
        print("Key is too short to preview safely.")

    if key.startswith("ghp_"):
        print("Key format: Starts with 'ghp_' (GitHub Personal Access Token - Legacy/Fine-grained?)")
    elif key.startswith("github_pat_"):
        print("Key format: Starts with 'github_pat_' (GitHub Personal Access Token - Fine-grained)")
    elif key.startswith("sk-"):
        print("Key format: Starts with 'sk-' (OpenAI Standard)")
    else:
        print("Key format: Unknown/Other")

if __name__ == "__main__":
    main()
