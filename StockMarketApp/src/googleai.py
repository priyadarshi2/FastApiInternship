import google.generativeai as genai

def gooogleAI(symb : str, txt : str):
    genai.configure(api_key="AIzaSyDJVMDPSsF7BGBIrd-RAgXoY4x3U55RdDk")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"answer me yes or no about this stock {symb} considering this meta description about the stock :\n {txt}")
    return str(response.text)