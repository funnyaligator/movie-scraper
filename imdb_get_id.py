# imdb_get_id.py
from bs4 import BeautifulSoup
import requests

def fetch_search_results(query):
    search_url = 'https://www.imdb.com/find'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    params = {
        'q': query,
        's': 'tt'  # Search type: tt for movies and TV series
    }
    
    response = requests.get(search_url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve search results. Status code: {response.status_code}")
        return None

def extract_first_movie_id(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the first <a> tag that contains the movie ID
    first_result = soup.find('a', href=True, class_='ipc-metadata-list-summary-item__t')
    
    if first_result and '/title/tt' in first_result['href']:
        href = first_result['href']
        movie_id = href.split('/title/tt')[1].split('/')[0]
        # print(movie_id)
        return movie_id
    else:
        return None

def get_movie_id(query):
    html_content = fetch_search_results(query)
    if html_content:
        return 'tt'+extract_first_movie_id(html_content)
    return None

# if __name__ == '__main__':
    # query = 'matrix'
    # movie_id = get_movie_id(query)
    # print(f"First movie ID: {movie_id}")

# print(get_movie_id('love'))