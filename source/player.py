from downloader import Downloader

class Player:
    class Item:
        def __init__(self, item, requester):
            self.item = item
            self.requester = requester

    def __init__(self, voice_client):
        self.voice_client = voice_client
        self.playing = None
        self.queue = []

    def play(self):
        self.playing = self.queue.pop(0)
        player = Downloader(self.playing.item.get_streams().get_audio_only().url)
        self.voice_client.play(player, after=self.after)
    
    def after(self, error):
        self.playing = None
        if len(self.queue) != 0:
            self.play()

    def add_item(self, item, requester):
        self.queue.append(Player.Item(item, requester))
        if not self.voice_client.is_playing():
            self.play()

    def skip_video(self):
        self.voice_client.stop()

    def stop(self):
        self.queue.clear()
        self.voice_client.stop()
