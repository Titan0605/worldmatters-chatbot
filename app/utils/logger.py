from loguru import logger
import sys

def setup_logger() -> None:
    logger.remove()
    logger.add(
        sys.stderr,
        level="DEBUG",
        format="{time:HH:mm:ss} | {level} | {extra[name]} | {message}",
        colorize=True,
        backtrace=True,
        diagnose=True
    )