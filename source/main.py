from bot import Bot
from config import Config

def main() -> int:
    config = Config()
    bot = Bot(config)

if __name__ == "__main__":
    result = main()
    exit(result)
