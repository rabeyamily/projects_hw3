import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()

# Get the OMDB API key from the environment variable
OMDb_API_KEY = os.getenv("OMDB_API_KEY")

# Scrape IMDB Top 25
def scrape_imdb():
    url = "https://www.imdb.com/chart/top/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, 'html.parser')

    movies = []
    for item in soup.select('li.ipc-metadata-list-summary-item'):
        title_element = item.select_one('h3.ipc-title__text')
        rating_element = item.select_one('span.ipc-rating-star--imdb')
        
        if title_element and rating_element:
            title = title_element.get_text(strip=True)
            # Remove rank number from title
            title = ' '.join(title.split()[1:])
            rating = rating_element.get_text(strip=True).split()[0]
            
            movies.append({'title': title, 'rating': rating})

    print(f"Total movies scraped: {len(movies)}")
    return pd.DataFrame(movies)

# Fetch data from OMDB API
def fetch_movie_data(title, api_key):
    params = {'t': title, 'apikey': api_key}
    response = requests.get("http://www.omdbapi.com/", params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch data for {title}. Status code: {response.status_code}")
        return {}

# Merge OMDB data with IMDB data
def merge_data(imdb_data, api_key):
    movie_data = []
    
    for index, movie in imdb_data.iterrows():
        print(f"Fetching data for: {movie['title']} ({index + 1}/{len(imdb_data)})")
        
        api_data = fetch_movie_data(movie['title'], api_key)
        if api_data:
            movie['box_office'] = api_data.get('BoxOffice', 'N/A')
            movie['awards'] = api_data.get('Awards', 'N/A')
            movie['genre'] = api_data.get('Genre', 'N/A')
            movie['director'] = api_data.get('Director', 'N/A')
        
        movie_data.append(movie)
        time.sleep(1)
    
    return pd.DataFrame(movie_data)

def clean_rating(rating):
    # Extract the numeric part before the parenthesis
    match = re.search(r'^(\d+(\.\d+)?)', str(rating))
    if match:
        return match.group(1)
    return rating

# Function to scrape and save data
def scrape_and_save_data():
    print("Starting IMDB scrape...")
    imdb_data = scrape_imdb()
    
    if imdb_data.empty:
        print("Failed to scrape IMDB data. Exiting.")
        return None

    print("Scraping complete. Now fetching additional data from OMDB...")
    final_data = merge_data(imdb_data, OMDb_API_KEY)
    
    if 'rating' in final_data.columns:
        # Clean the rating column
        final_data['rating'] = final_data['rating'].apply(clean_rating)
        
        # Convert to float and handle any remaining non-convertible values
        final_data['rating'] = pd.to_numeric(final_data['rating'], errors='coerce')
        
        # Drop rows where rating is NaN after conversion
        final_data.dropna(subset=['rating'], inplace=True)
    else:
        print("'rating' column not found in the scraped data.")
    
    final_data.to_csv("cleaned_movie_data.csv", index=False)
    print("Data successfully saved to 'cleaned_movie_data.csv'.")
    return final_data

# Function to display movie names
def display_movie_names(data, count):
    print(f"\nTop {count} Movies:")
    for i, title in enumerate(data['title'][:count], 1):
        print(f"{i}. {title}")

# Function to display movie details in box style
def display_movie_details(data, title):
    movie = data[data['title'] == title].iloc[0]
    print("\n" + "=" * 40)
    print(f"Title: {movie['title']}")
    print(f"Rating: {movie['rating']}")
    print(f"Director: {movie['director']}")
    print(f"Genre: {movie['genre']}")
    print(f"Awards: {movie['awards']}")
    print(f"Box Office: {movie['box_office']}")
    print("=" * 40)

#menu function
def interactive_menu(data):
    while True:
        print("\nOptions:")
        print("1. Show movie names list")
        print("2. Show movie details")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            while True:
                try:
                    count = int(input("How many movies do you want to see? (1-25): "))
                    if 1 <= count <= 25:
                        break
                    else:
                        print("Please enter a number between 1 and 25.")
                except ValueError:
                    print("Please enter a valid number.")
            display_movie_names(data, count)
        
        elif choice == '2':
            title = input("Enter the movie title: ")
            if title in data['title'].values:
                display_movie_details(data, title)
            else:
                print("Movie not found.")
        
        elif choice == '3':
            print("Thank you for using the movie database. Have a good one!")
            break
        
        else:
            print("Invalid choice. Please try again.")

# Main execution
if __name__ == "__main__":
    movie_data = scrape_and_save_data()
    if movie_data is not None:
        interactive_menu(movie_data)
    else:
        print("Failed to scrape and save data. Exiting.")