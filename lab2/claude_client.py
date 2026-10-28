from dotenv import load_dotenv
import anthropic

load_dotenv()  # loads ANTHROPIC_API_KEY from a .env file in your project root
client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env