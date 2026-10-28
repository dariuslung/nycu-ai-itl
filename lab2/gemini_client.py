from dotenv import load_dotenv
from google import genai
import os

load_dotenv()  # loads GOOGLE_API_KEY from a .env file in your project root
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])