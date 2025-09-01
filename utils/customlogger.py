import os
import logging
from logging import Logger
from logging.handlers import RotatingFileHandler


class CustomLogger:
    def __init__(
        self,
        name: str,
        log_file: str,
        logs_dir: str="./logs",
        level: int=logging.INFO,
    ) -> None:
        # Ensure logs directory exists
        self.logs_dir = logs_dir
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir, exist_ok=True)

        # Always ensure .log extension
        if not log_file.endswith(".log"):
            log_file += ".log"
        log_path = os.path.join(self.logs_dir, log_file)

        # Configure logger
        self.logger: Logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.propagate = False  # prevent duplicate logs

        # Avoid duplicate handlers if logger is created multiple times
        if not self.logger.handlers:
            handler = RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=5)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def get_logger(self) -> Logger:
        """Return the configured logger instance."""
        return self.logger
