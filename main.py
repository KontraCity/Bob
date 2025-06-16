from bot import Bot
from config import Config

def main() -> int:
    bot = Bot(Config())
    bot.run()
    return 0

if __name__ == "__main__":
    result = main()
    exit(result)
