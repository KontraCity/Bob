from bot import Bot
from config import Config

def main() -> int:
    config = Config()
    bot = Bot(config)
    return 0

if __name__ == "__main__":
    result = main()
    exit(result)
