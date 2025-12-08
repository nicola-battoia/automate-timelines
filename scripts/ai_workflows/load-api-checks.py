# app.py
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API key
API_KEY = os.environ.get("OPENAI_API_KEY")

if not API_KEY:
    print("Please set OPENAI_API_KEY in .env file")
    exit(1)

# Use the API
headers = {"Authorization": f"Bearer {API_KEY}"}
# Make your API calls...
