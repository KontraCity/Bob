import datetime
import random
import discord
import youtube

def embed(color: discord.Color, emoji: str, phrase: str, comment: str = None, override: bool = False) -> discord.Embed:
    embed = discord.Embed()
    embed.color = color
    phrase_str = comment if override else (f"{phrase}, boss. {comment}." if comment else f"{phrase}, boss.")
    embed.description = f"{emoji} **{phrase_str}**"
    return embed

def length_str(length: datetime.timedelta) -> str:
    hours, remainder = divmod(length.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)

    if not hours:
        return f"{int(minutes)}:{int(seconds):02}"
    return f"{int(hours)}:{int(minutes):02}:{int(seconds):02}"

def good_embed(comment: str = None, override: bool = False) -> discord.Embed:
    phrase = random.choice([
        "Yes",
        "Alright",
        "Right away",
        "On it",
        "Got it",
        "Will do",
        "Consider it done",
        "Absolutely",
        "Sure thing",
        "Of course",
        "As you wish",
        "No problem",
        "Understood",
        "I'm on it",
    ])
    return embed(discord.Color.dark_green(), "✅", phrase, comment, override)
   
def bad_embed(comment: str = None, override: bool = False) -> discord.Embed:
    phrase = random.choice([
        "Can't do",
        "No can do",
        "Negative",
        "That's a no",
        "Nope",
        "Not gonna happen"
    ])
    return embed(discord.Color.red(), "❌", phrase, comment, override)

def error_embed(comment: str = None, override: bool = False) -> discord.Embed:
    phrase = random.choice([
        "Bad news",
        "We’ve got a problem",
        "Something went wrong",
        "This might be an issue",
        "Got a bit of a setback",
        "Slight complication",
        "Things didn’t go as planned"
    ])
    return embed(discord.Color.dark_red(), "💀", phrase, comment, override)

def video_embed(video: youtube.Video) -> discord.Embed:
    embed = good_embed("Video added to queue") 
    embed.add_field(name=f"{video.title} [{length_str(video.length)}]", value="")
    embed.set_thumbnail(url=video.thumbnail_url)
    return embed
