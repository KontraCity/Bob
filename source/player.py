from downloader import Downloader

class Player:
    def __init__(self, voice_client, item=None):
        self.voice_client = voice_client
        self.queue = []

        if item:
            self.queue.append(item)
            self.play()

    def after(self, error):
        if len(self.queue) != 0:
            self.play()

    def play(self):
        item = self.queue.pop()
        player = Downloader(item.get_streams().get_audio_only().url)
        self.voice_client.play(player, after=self.after)
    
    def add_item(self, item):
        self.queue.append(item)
        if not self.voice_client.is_playing():
            self.play()

    def skip_video(self):
        self.voice_client.stop()

    def stop(self):
        self.queue.clear()
        self.voice_client.stop()
