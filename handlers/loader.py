from aiogram import types
from core.services.film_search_engine import FilmSearchEngine

film_search_engine = FilmSearchEngine()
command_descriptions = [
    types.BotCommand(command="/help", description="Get info about bot"),
    types.BotCommand(command="/start", description="start using the bot"),
    types.BotCommand(command="/stats", description="find out search statistics"),
    types.BotCommand(command="/history", description="find out search history"),
]
