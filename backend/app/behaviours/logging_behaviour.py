from typing import Any, Callable
from app.utils.logger import get_logger

logger = get_logger(__name__)


class LoggingBehaviour:
    """
    Pipeline behaviour that logs every command before and after execution.
    Runs automatically for every command sent through the mediator.
    """

    def handle(self, command: Any, next_fn: Callable) -> Any:
        command_name = type(command).__name__
        logger.info(f"Handling {command_name}")
        try:
            response = next_fn()
            logger.info(f"Handled {command_name} successfully")
            return response
        except Exception as e:
            logger.error(f"Error handling {command_name}: {str(e)}")
            raise
