import logging

def configureLogger(logger: logging.Logger) -> None:
    formatter = logging.Formatter("[{asctime}] [{levelname:^8}] {name}: {message}", datefmt="%d.%m.%C %H:%M:%S", style="{")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.handlers = [handler]
