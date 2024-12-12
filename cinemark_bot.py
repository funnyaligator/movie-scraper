#TOKEN: Final = "6403479380:AAEd29OZd6lyia8gycq84vhmNLIos-cNZ0M"
#from typing import Final

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from scraper import get_movies  # Import the updated scraper function
from typing import Final

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN: Final = "6403479380:AAEd29OZd6lyia8gycq84vhmNLIos-cNZ0M"

logger = logging.getLogger(__name__)

# Define a start command function
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! Use /movies to get the latest showtimes.')

# Define the movies command function
async def movies(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Fetch movie data using your scraper
    movie_data = get_movies()
    
    # Format the movie data into a message string
    message = ""
    for movie in movie_data:
        movie_info = f"{movie['title']} | {movie['year']} | {movie['rating']} | {movie['genre']} | {movie['actors']}\n    Showtimes: {', '.join(movie['showtimes'])}\n\n"
        message += movie_info
    
    # Send the formatted movie data to the user
    await update.message.reply_text(message if message else "No movies available.",parse_mode='HTML')

# Define the main function to start the bot
def main() -> None:
    # Replace 'YOUR_API_TOKEN' with your actual bot token
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("movies", movies))

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()
