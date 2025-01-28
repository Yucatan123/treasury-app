import requests
from bs4 import BeautifulSoup

# Define the target URL
URL = "https://www.cnbc.com/quotes/US10Y"

def get_treasury_yield():
    # Fetch the page content
    response = requests.get(URL)
    response.raise_for_status()  # Raise an error for bad responses
    
    # Parse HTML content
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract the treasury yield using the correct CSS selector
    yield_value = soup.find("span", class_="QuoteStrip-lastPrice").text
    print(f"10-Year Treasury Yield: {yield_value}")
    
    return yield_value

if __name__ == "__main__":
    get_treasury_yield()
