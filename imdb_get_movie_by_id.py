# imdb_movie_CHATGPT.py
# import imdb_get_id
import requests
from bs4 import BeautifulSoup
import json

class IMDbScraper:
    def __init__(self):
        self.base_url = 'https://www.imdb.com/title/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        }

    def fetch_movie_page(self, movie_id):
        url = f'{self.base_url}{movie_id}/'
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to retrieve page. Status code: {response.status_code}")
            return None

    def extract_details(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract title and year from the <title> tag
        title_tag = soup.find('title')
        if title_tag:
            title_text = title_tag.text.strip()
            title = title_text.split(' (')[0]
            year = title_text.split(' (')[1].split(')')[0] if '(' in title_text else 'N/A'
        else:
            title = 'N/A'
            year = 'N/A'

        # Extract JSON-LD data
        json_ld_script = soup.find('script', type='application/ld+json')
        if json_ld_script:
            try:
                json_data = json.loads(json_ld_script.string)
                rating = json_data.get('aggregateRating', {}).get('ratingValue', 'N/A')
                genre = ', '.join(json_data.get('genre', []))
                actors = ', '.join([actor.get('name') for actor in json_data.get('actor', [])])
            except json.JSONDecodeError:
                print("Error decoding JSON-LD data")
                rating = 'N/A'
                genre = 'N/A'
                actors = 'N/A'
        else:
            rating = 'N/A'
            genre = 'N/A'
            actors = 'N/A'

        return {
            'title': title,
            'year': year,
            'rating': rating,
            'genre': genre,
            'actors': actors
        }

    def scrape(self, movie_id):
        html_content = self.fetch_movie_page(movie_id)
        if html_content:
            return self.extract_details(html_content)
        return None

def get_movie_details(name):
    from imdb_get_id import get_movie_id  # Import the function from the first file
    
    movie_id = get_movie_id(name)
    
    if movie_id:
        scraper = IMDbScraper()
        movie_details = scraper.scrape(movie_id)
        if movie_details:
            # print(movie_details)
            return list(movie_details.values())
    else:
        # print("Movie ID not found.")
        return "Movie ID not found."
    

# print(get_movie_details('samurai last'))
