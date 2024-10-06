# IMDB Top Movies Data Pipeline

This project creates a unique dataset by combining IMDB's top-rated movies with detailed information from the OMDB API. It offers a comprehensive view of highly-rated films, including box office performance, awards, and other key details not readily available in a single dataset.

## Features

1. **Web Scraping**: Automatically scrapes the IMDB Top 250 list to get the latest top-rated 25 movies and their ratings.

2. **API Integration**: Utilizes the OMDB API to fetch additional detailed information for each movie.

3. **Data Cleaning**: Implements data cleaning processes, particularly for movie ratings, to ensure data accuracy and consistency.

4. **Comprehensive Movie Data**: Combines data from multiple sources to provide a rich dataset including:
   - Movie title
   - IMDB rating
   - Box office earnings
   - Awards received
   - Genre
   - Director

5. **Interactive Menu**: Offers a user-friendly command-line interface with options to:
   - Display a list of top movies (user can specify the number of movies to view)
   - Show detailed information for a specific movie
   - Exit the program

6. **Data Export**: Automatically saves the cleaned and combined data to a CSV file for easy analysis and sharing.

7. **Error Handling**: Implements robust error handling for web scraping and API requests to ensure smooth execution.

8. **Rate Limiting**: Incorporates rate limiting for API requests to respect usage limits and prevent overloading of services.

9. **Environment Variable Support**: Uses a .env file for secure storage of API keys, enhancing security and portability.

## Data Sources

1. IMDB Top 250 List: We scrape this list to get the top-rated 25 movies and their IMDB ratings.
2. OMDB API: We use this API to fetch additional details for each movie, such as box office earnings, awards, genre, and director.

## Value Proposition

This dataset provides unique value by:

1. Combining high-quality ratings data from IMDB with detailed movie information from OMDB.
2. Offering a curated list of top-rated movies with comprehensive details, saving researchers and movie enthusiasts significant time in data collection.
3. Providing box office data alongside critical acclaim, allowing for analysis of the relationship between movie quality and commercial success.
4. Enabling genre-based analysis of top-rated movies, which can reveal trends in film appreciation over time.

While individual pieces of this data are available separately, our dataset uniquely combines these elements into a single, easy-to-use format, making it a valuable resource for film studies, data analysis projects, and movie recommendation systems.

## Installation and Usage

1. Clone this repository: git clone git@github.com:rabeyamily/projects_hw3.git

2. Set up a virtual environment and activate it: python -m venv venv
source venv/bin/activate # On Windows, use venv\Scripts\activate 

3. Install the required packages:pip install -r requirements.txt

4. Create a `.env` file in the project root and add your OMDB API key: i.e OMDB_API_KEY = 1067f036 (this is my API Key)

5. Run the script:python main.py

6. Follow the interactive menu to explore the data or generate the CSV file.

## Output

The script generates a CSV file named `cleaned_movie_data.csv` containing the combined and cleaned data from IMDB and OMDB.

