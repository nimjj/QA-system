import os
import re
import json
import logging
from datetime import datetime, timezone
from logging.handlers import TimedRotatingFileHandler

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LOG_DIR = os.path.join(_ROOT, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "app.log")


def log_namer(default_name: str) -> str:
    """Rename rotated log from app.log.YYYY-MM-DD to YYYY-MM-DD.log in logs folder."""
    dir_name, base_name = os.path.split(default_name)
    match = re.search(r"app\.log\.(\d{4}-\d{2}-\d{2})", base_name)
    if match:
        date_str = match.group(1)
        return os.path.join(dir_name, f"{date_str}.log")
    return default_name


class JsonLineFormatter(logging.Formatter):
    """Formats all log records as clean single-line JSON objects."""

    def format(self, record: logging.LogRecord) -> str:
        if isinstance(record.msg, dict):
            raw_data = record.msg
        else:
            msg = record.getMessage()
            try:
                parsed = json.loads(msg)
                if isinstance(parsed, dict):
                    raw_data = parsed
                else:
                    raw_data = {"message": msg}
            except Exception:
                raw_data = {"message": msg}

        ordered = {
            "timestamp": raw_data.get("timestamp", datetime.now(timezone.utc).isoformat()),
            "log_type": raw_data.get("log_type", "APP")
        }

        # Include standard audit fields in structured order
        for field in ["correlation_id", "actor", "request", "response"]:
            if field in raw_data:
                ordered[field] = raw_data[field]

        # Add remaining fields, explicitly skipping service, environment, and level
        ignored_keys = {"service", "environment", "level"}
        for k, v in raw_data.items():
            if k not in ordered and k not in ignored_keys:
                ordered[k] = v

        # Strictly output one line without unescaped newlines
        return json.dumps(ordered, ensure_ascii=False)


def get_logger(name: str = "qa_service") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = JsonLineFormatter()

        file_handler = TimedRotatingFileHandler(
            filename=LOG_FILE,
            when="midnight",
            interval=1,
            backupCount=30,
            encoding="utf-8"
        )
        file_handler.suffix = "%Y-%m-%d"
        file_handler.namer = log_namer
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        logger.propagate = False

    return logger


logger = get_logger("qa_service")
