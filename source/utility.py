import logging

def configureLogger(logger: logging.Logger) -> None:
    class Formatter(logging.Formatter):
        def format(self, record):
            level_map = {
                "DEBUG": "D",
                "INFO": "I",
                "WARNING": "W",
                "ERROR": "E",
                "CRITICAL": "C"
            }

            level_letter = level_map.get(record.levelname, "?")
            record.levelletter = level_letter
            return super().format(record)

    formatter = Formatter("[{asctime} {levelletter}] [{name}] {message}", datefmt="%d.%m.%C %H:%M:%S", style="{")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.handlers = [handler]
