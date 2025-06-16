from config import Config

def main() -> int:
    config = Config()
    print(f"Bot token: {config.getToken()}")
    return 0

if __name__ == "__main__":
    try:
        result = main()
        exit(result)
    except Exception as error:
        print("Fatal exception occured!")
        print(f"Message: {error}")
        exit(1)
