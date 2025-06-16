import json

class Config:
    FILENAME = "config.json"
    def __init__(self):
        try:
            with open(Config.FILENAME, "r") as file:
                data = json.load(file)
                self.token = data["token"]
        except Exception:
            raise Exception(f"Couldn't read and parse config file \"{Config.FILENAME}\"")

    def getToken(self) -> str:
        return self.token
