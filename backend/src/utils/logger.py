import logging
import os
from pathlib import Path

from src.settings import app_settings


class ExtraFormatter(logging.Formatter):
    """Custom formatter that includes extra fields in log output."""

    def format(self, record):
        # Get the standard formatted message
        msg = super().format(record)

        # Add extra fields if they exist
        extra_fields = []
        for key, value in record.__dict__.items():
            # Skip standard logging fields
            if key not in [
                "name",
                "msg",
                "args",
                "levelname",
                "levelno",
                "pathname",
                "filename",
                "module",
                "lineno",
                "funcName",
                "created",
                "msecs",
                "relativeCreated",
                "thread",
                "threadName",
                "processName",
                "process",
                "message",
                "exc_info",
                "exc_text",
                "stack_info",
                "asctime",
            ]:
                extra_fields.append(f"{key}={value}")

        if extra_fields:
            msg += f" | EXTRA: {', '.join(extra_fields)}"

        return msg


def get_logger(logger_name: str, logs_dir: Path = None):

    logs_dir = app_settings.log.logs_dir

    log_filename = f"log_{app_settings.log.run_timestamp}.log"
    logs_output_fp = logs_dir / log_filename

    logger = logging.getLogger(logger_name)

    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger

    logger.setLevel(app_settings.log.log_level)

    os.makedirs(logs_dir, exist_ok=True)

    file_handler = logging.FileHandler(logs_output_fp)
    file_handler.setLevel(app_settings.log.log_level)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(app_settings.log.log_level)

    formatter = logging.Formatter(fmt=app_settings.log.log_format, datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
