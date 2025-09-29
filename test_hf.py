# test_hf.py
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")

if not HF_API_KEY:
    print("ERROR: HF_API_KEY not found in environment variables")
    print("Make sure you have a .env file with HF_API_KEY=your_api_key")
else:
    print(f"Found HF_API_KEY: {HF_API_KEY[:10]}...")  # Show first 10 chars for security

client = InferenceClient(api_key=HF_API_KEY)

try:
    response = client.text_generation(
        model="facebook/bart-large-cnn",
        prompt="Summarize this: The Kochi Metro is a rapid transit system serving the city of Kochi, Kerala.",
        max_new_tokens=50,
    )
    print("HuggingFace API response:", response)
except Exception as e:
    print("HuggingFace API error:", str(e))
    import traceback
    traceback.print_exc()