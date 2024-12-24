import google.generativeai as genai
import os 
from dotenv import load_dotenv

load_dotenv()

def gooogleAI(symb : str, txt : str):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"answer me yes or no about this stock {symb} considering this meta description about the stock :\n {txt}")
    return str(response.text)