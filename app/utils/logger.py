from loguru import logger
import sys

def setup_logger() -> None:
    """Configure the logger."""
    logger.remove()
    
    logger.add(
        sys.stdout,
        level="DEBUG",
        format=(
            "<green>{time:HH:mm:ss.SSS}</green> "
            "<dim>│</dim> "
            "<level>{level: <8}</level> "
            "<dim>│</dim> "
            "<magenta>{extra[name]}</magenta>:<cyan>{function}</cyan>:<yellow>{line}</yellow> "
            "<dim>│</dim> "
            "{message}"
        ),
        colorize=True,
        backtrace=True,
        diagnose=True,
        enqueue=True
    )