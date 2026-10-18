import logging.config
from typing import Dict, Any


def configure_logging(level: str = "INFO") -> None:
    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {"format": "%(asctime)s %(levelname)s %(name)s %(message)s"}
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": level.upper(),
            }
        },
        "root": {"handlers": ["console"], "level": level.upper()},
    })
