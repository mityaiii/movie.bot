__all__ = ['routes', 'command_descriptions']

from handlers.commands.help import router as help_router
from handlers.commands.start import router as start_router
from handlers.commands.stats import router as stats_router
from handlers.commands.history import router as history_router
from handlers.different_types.text_handler import router as text_router

from handlers.loader import command_descriptions

routes = (help_router, stats_router, start_router, history_router, text_router)
