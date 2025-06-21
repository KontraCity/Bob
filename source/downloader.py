import requests
import av
import discord
import discord.opus
if not discord.opus.is_loaded():
    discord.opus.load_opus('./libopus.so')

class Downloader(discord.AudioSource):
    @staticmethod
    def stream_pcm(url):
        class StreamBuffer:
            def __init__(self, url):
                response = requests.get(url, stream=True)
                response.raise_for_status()
                self.buffer = bytearray()
                self.iterator = response.iter_content(chunk_size=4096)
                
            def read(self, size=-1):
                while len(self.buffer) < size or size == -1:
                    try:
                        chunk = next(self.iterator)
                        self.buffer.extend(chunk)
                    except StopIteration:
                        break
                if size == -1:
                    size = len(self.buffer)

                result, self.buffer = self.buffer[:size], self.buffer[size:]
                return bytes(result)

        stream_buffer = StreamBuffer(url)
        container = av.open(stream_buffer)
        audio_stream = max(container.streams.audio, key=lambda s: s.bit_rate or 0)
        if audio_stream is None:
            raise Exception("No audio stream found")

        resampler = av.audio.resampler.AudioResampler(format="s16", layout="stereo", rate=48000)
        for packet in container.demux(audio_stream):
            for frame in packet.decode():
                for resampled_frame in resampler.resample(frame):
                    pcm_bytes = bytes(resampled_frame.planes[0])
                    length = resampled_frame.samples * 2 * 2
                    yield pcm_bytes[:length]
        for flushed_frame in resampler.resample(None):
            pcm_bytes = bytes(flushed_frame.planes[0])
            length = flushed_frame.samples * 2 * 2
            yield pcm_bytes[:length]
    
    def __init__(self, url):
        self.frame_size = 960 * 2 * 2
        self.buffer = b""
        self.iterator = iter(Downloader.stream_pcm(url))
        self.closed = False

    def read(self):
        while len(self.buffer) < self.frame_size and not self.closed:
            try:
                chunk = next(self.iterator)
            except StopIteration:
                self.closed = True
                break

            if not chunk:
                self.closed = True
                break
            self.buffer += chunk

        if len(self.buffer) == 0:
            return b""

        output, self.buffer = self.buffer[:self.frame_size], self.buffer[self.frame_size:]
        return output

    def is_opus(self):
        # Providing PCM, not Opus
        return False

    def cleanup(self):
        self.closed = True
