import requests
import re
import imdb_get_movie_by_id
import concurrent.futures
from datetime import datetime
import html
import urllib.parse

# Constants
DATETODAY = datetime.now().strftime('%Y-%m-%d')
URL = f'https://www.cinemark.com/theatres/fl-orlando/cinemark-orlando-and-xd?utm_medium=organic&utm_source=gmb&utm_campaign=int&utm_content=GMB_listing&y_source=1_MTc0OTMxMDYtNzE1LWxvY2F0aW9uLmdvb2dsZV93ZWJzaXRlX292ZXJyaWRl&showDate={DATETODAY}'
PATTERN = r"(<h3 id=.\d\d\d\d\d.>.*?<\/h3>|\d\d:\d\d:\d\d\">\d?\d:\d\d[A|P|a|p][M|m])"

def fetch_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        return response.content.decode('utf-8')
    except requests.RequestException as e:
        print(f"Error fetching page content: {e}")
        return None

def generate_youtube_trailer_link(title: str) -> str:
    query = urllib.parse.quote_plus(title)
    return f'https://www.youtube.com/results?search_query={query}'

def extract_times_and_titles(content):
    if not content:
        return [], []

    content = html.unescape(content)
    matches = re.findall(PATTERN, content, re.IGNORECASE)
    
    movies_list = []
    times_list = []
    times = ''
    time = ''
    
    for match in matches:
        if 'h3 id' in match:
            title = re.sub("<.*?>", "", match).strip()
            if time:
                sorted_times = sort_times(times)
                movies_list.append(title)
                times_list.append(sorted_times)
                times = ''
            else:
                movies_list.append(title)
                times_list.append('no time')
        else:
            time = re.sub("<.*?>", "", match).strip()
            timeF = time[10:] if len(time) > 10 else time
            times += timeF + ' '
            if match == matches[-1]:
                sorted_times = sort_times(times)
                times_list.append(sorted_times)
                times = ''
    
    # Clean titles
    movies_list = [re.sub(r'\(.*\)', '', title).strip() for title in movies_list]
    
    # Remove 'no time' entries if present
    if times_list and times_list[0] == 'no time':
        times_list.pop(0)
    
    return movies_list, times_list

def sort_times(times):
    hours = times.split()
    am1group, am2group, pm1group, pm2group = [[] for _ in range(4)]
    
    for h in hours:
        if len(h) == 6:
            if h[4] == 'a':
                am1group.append(h)
            elif h[4] == 'p':
                pm1group.append(h)
        elif len(h) == 7:
            if h[5] == 'a':
                am2group.append(h)
            elif h[5] == 'p':
                pm2group.append(h)
    
    sorted_hours = sorted(am1group) + sorted(am2group) + sorted(pm1group) + sorted(pm2group)
    return ' '.join(sorted_hours)

def scrape_movie_details(movies_list, times_list):
    movie_details = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(imdb_get_movie_by_id.get_movie_details, movies_list)
        
        for imdb, time in zip(results, times_list):
            if imdb:
                m_title, m_year, m_rating, m_genre, m_actors = imdb
                movie_link = f'<a href="{generate_youtube_trailer_link(m_title)}">{m_title}</a>'
                details = {
                    'title': movie_link,
                    'year': m_year,
                    'rating': m_rating,
                    'genre': m_genre,
                    'actors': m_actors,
                    'showtimes': time.split()
                }
                movie_details.append(details)
    return movie_details

def get_movies():
    content = fetch_page_content(URL)
    movies_list, times_list = extract_times_and_titles(content)
    return scrape_movie_details(movies_list, times_list)

if __name__ == '__main__':
    movies = get_movies()
    for movie in movies:
        print(f"{movie['title']} | {movie['year']} | {movie['rating']} | {movie['genre']} | {movie['actors']}")
        print(f"    Showtimes: {', '.join(movie['showtimes'])}")
