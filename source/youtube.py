import re, datetime
import pytubefix

class Video:
    class Chapter:
        def __init__(self, title: str, timestamp: int, duration: int, thumbnail_url: str):
            self.title = title
            self.timestamp = datetime.timedelta(seconds=timestamp)
            self.duration = datetime.timedelta(seconds=duration)
            self.thumbnail_url = thumbnail_url

    class Block:
        def __init__(self, timestamp: int, duration: int, intensity: float):
            self.timestamp = datetime.timedelta(seconds=timestamp)
            self.duration = datetime.timedelta(seconds=duration)
            self.intensity = intensity

    @staticmethod
    def validate_id(id: str) -> bool:
        matches = re.match(r"^([^\"&?\/\s]{11})$", id)
        return matches is not None

    @staticmethod
    def extract_id(url: str) -> str:
        if Video.validate_id(url):
            return url
        regex = r"youtu(?:be\.com|\.be)\/(?:(?:watch(?:_popup)?\?v=)|(?:embed\/)|(?:live\/)|(?:shorts\/))?([^\"&?\/\s]{11})"
        matches = re.search(regex, url)
        return matches.group(1) if matches else None

    @staticmethod
    def from_url(url: str) -> "Video":
        video_id = Video.extract_id(url)
        if video_id is None:
            raise Exception("Invalid video ID or URL")

        video = pytubefix.YouTube(f"https://www.youtube.com/watch?v={video_id}")
        return Video(video)

    @staticmethod
    def from_query(url: str) -> "Video":
        search = pytubefix.Search(url)
        if len(search.videos) == 0:
            raise Exception("No results")
        return Video(search.videos[0])

    def __init__(self, video: pytubefix.YouTube):
        self._video = video
        self.video_id = video.video_id
        self.watch_url = video.watch_url
        self.title = video.title
        self.author = video.author
        self.length = datetime.timedelta(seconds=video.length)
        self.thumbnail_url = video.thumbnail_url
        self.views = video.views
        self.upload_date = video.publish_date
        self.chapters = [Video.Chapter(c.title, c.start_seconds, c.duration, c.thumbnails[-1].url) for c in video.chapters]
        self.heatmap = [Video.Block(b["start_seconds"], b["duration"], b["norm_intensity"]) for b in video.replayed_heatmap]

    def get_streams(self) -> pytubefix.StreamQuery:
        return self._video.streams

class Playlist:
    @staticmethod
    def validate_id(id: str) -> bool:
        matches = re.match(r"^(PL[^\"&?\/\s]{16,32}$|^OLAK5uy_[^\"&?\/\s]{33})$", id)
        return matches is not None

    @staticmethod
    def extract_id(url: str) -> str:
        if Playlist.validate_id(url):
            return url
        regex = r"(youtube\.com\/(?:playlist\?list=|watch\?v=[^\"&?\/\s]{11}&list=)(PL[^\"&?\/\s]{16,32}|OLAK5uy_[^\"&?\/\s]{33}))";
        matches = re.search(regex, url)
        return matches.group(1) if matches else None

    @staticmethod
    def from_url(url: str) -> "Playlist":
        playlist_id = Playlist.extract_id(url)
        if playlist_id is None:
            raise Exception("Invalid playlist ID or URL")

        playlist = pytubefix.Playlist(playlist_id)
        return Playlist(playlist)

    def __init__(self, playlist: pytubefix.Playlist):
        def get_videos(playlist_videos):
            for video in playlist_videos:
                yield Video(video)
    
        self.view_url = playlist.playlist_url
        self.title = playlist.title
        self.owner = playlist.owner
        self.length = playlist.length
        self.thumbnail_url = playlist.thumbnail_url
        self.views = playlist.views
        self.videos = pytubefix.helpers.DeferredGeneratorList(get_videos(playlist.videos))
