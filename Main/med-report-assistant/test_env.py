from dotenv import load_dotenv
import os

load_dotenv()

print("ENV KEY:", os.getenv("OPENAI_API_KEY"))
