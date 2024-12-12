# Movie Scraper

A Python app for scraping movie names from a local movie theater website and using concurrent futures to find ratings on IMDb. The results are then sent to a Telegram bot, allowing users to request movie ratings by simply texting the bot.

## Features
- Scrapes movie names from a local movie theater.
- Uses **concurrent futures** to efficiently fetch IMDb ratings for movies in parallel.
- Sends the movie names and ratings to a **Telegram bot**.
- Users can interact with the bot and request movie ratings by sending text commands.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/funnyaligator/movie-scraper.git
   cd movie-scraper
