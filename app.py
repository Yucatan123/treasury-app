import requests
from bs4 import BeautifulSoup
import os
import psycopg2
from psycopg2 import sql
from datetime import datetime

# Define the target URL
URL = "https://www.cnbc.com/quotes/US10Y"

# Fetch the treasury yield
def get_treasury_yield():
    try:
        # Fetch the page content
        response = requests.get(URL)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract the treasury yield using the correct CSS selector
        yield_value = soup.find("span", class_="QuoteStrip-lastPrice").text.strip()
        print(f"10-Year Treasury Yield: {yield_value}")
        
        # Save to database (store the yield along with timestamp)
        save_to_db(yield_value)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

# Save the yield value to the database
def save_to_db(yield_value):
    try:
        # Get the environment variables
        db_host = os.getenv("DB_HOST")
        db_name = os.getenv("DB_NAME")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_port = os.getenv("DB_PORT", 5432)

        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            port=db_port
        )
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS treasury_yield (
                id SERIAL PRIMARY KEY,
                yield_value VARCHAR(255),
                timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Insert the yield data into the database
        cursor.execute(
            sql.SQL("INSERT INTO treasury_yield (yield_value) VALUES (%s)"),
            [yield_value]
        )
        conn.commit()
        print("Yield value saved to the database.")

        # Close the database connection
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error saving data to the database: {e}")

# Main function for the cron job
def main():
    get_treasury_yield()

if __name__ == "__main__":
    main()
