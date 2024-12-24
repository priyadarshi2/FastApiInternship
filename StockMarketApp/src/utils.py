import requests
from fastapi import HTTPException
from bs4 import BeautifulSoup

def get_articles(symb : str):
    # Your API Key
    API_KEY = "4c30eab85fe84820866ade873c97448d"

    # News API endpoint for searching articles
    BASE_URL = "https://newsapi.org/v2/everything"

    # Stock symbol or company name to search
    stock_query = symb

    #set the limit of the fetched articles to 5
    article_limit = 5

    # Parameters for the request
    params = {
        "q": stock_query,           # Query term (stock name or symbol)
        "language": "en",           # Language of the news (e.g., 'en' for English)
        "sortBy": "publishedAt",    # Sort results by relevance or publishedAt
        "pageSize" : article_limit, # Set the limit of the articles to be fetched 
        "apiKey": API_KEY,          # Your News API key
    }

    # Make the API request
    response = requests.get(BASE_URL, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON
        news_data = response.json()
        articles = news_data.get("articles", [])
        return articles
    else:
        print(f"Error: Unable to fetch news (Status Code: {response.status_code})")
    
def fetch_articles(symb : str):
    articles = get_articles(symb)

    if articles:
        texts = ""
        for idx, article in enumerate(articles, start=1):
            article_url = article['url']
            try:
                # Request the article's webpage
                article_response = requests.get(article_url, timeout=10)
                if article_response.status_code == 200:
                    soup = BeautifulSoup(article_response.content, "html.parser")
                    
                    # Extract the main content (refine based on publisher's structure)
                    paragraphs = soup.find_all("p")
                    full_text = " ".join(p.get_text() for p in paragraphs)  
                else:
                    print("   Could not fetch the full article content.")
            except Exception as e:
                raise HTTPException(status_code=404, detail = f'{e}')
        return full_text
    else:
        raise HTTPException(status_code=200, detail="Information not available")
    
