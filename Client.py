from dotenv import load_dotenv
from google import genai
import os

load_dotenv()
client = genai.Client(api_key=os.environ.get("GENAI_API_KEY"))

#def process_query(query: str):

    
    

