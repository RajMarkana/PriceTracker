from tracker import PriceTracker
import logging
import colorlog
import os

os.makedirs("logs", exist_ok=True)
console_handler = colorlog.StreamHandler()
console_handler.setFormatter(
    colorlog.ColoredFormatter(
        "%(log_color)s[%(levelname)s] %(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )
)

file_handler = logging.FileHandler("logs/tracker.log", encoding="utf-8")
file_handler.setFormatter(
    logging.Formatter(
        "[%(levelname)s] %(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
)

logger = colorlog.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
logger.addHandler(file_handler)


if __name__ == "__main__":
    tracker = PriceTracker()
    tracker.schedule_checks()
