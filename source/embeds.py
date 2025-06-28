import datetime
import random
import discord
import player
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

def cardinal(word: str, number: int) -> str:
    if number == 1:
        return word
    return f"{word}s"

def views_str(views: int) -> str:
    if views >= 1_000_000_000_000:
        return f"{views // 1_000_000_000_000}T views"
    elif views >= 1_000_000_000:
        return f"{views // 1_000_000_000}B views"
    elif views >= 1_000_000:
        return f"{views // 1_000_000}M views"
    elif views >= 1_000:
        return f"{views // 1_000}K views"
    else:
        return f"{views} {cardinal('view', views)}"

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
    embed.add_field(name=video.title, value=f"by {video.author}, {views_str(video.views)} [{length_str(video.length)}]")
    embed.set_thumbnail(url=video.thumbnail_url)
    return embed

def queue_embed(player: player.Player) -> discord.Embed:
    embed = discord.Embed()
    embed.color = discord.Color.dark_green()

    if player.playing:
        embed.description = f"🎶 **Playing {player.playing.item.title}**"
        embed.description += f"\nby {player.playing.item.author}, {views_str(player.playing.item.views)} [{length_str(player.playing.item.length)}]"
        embed.description += f"\nrequested by <@{player.playing.requester.id}>"
        embed.set_thumbnail(url=player.playing.item.thumbnail_url)
    else:
        embed.description = "🥱 **Nothing is playing, boss**"

    if len(player.queue) > 0:
        playtime = length_str(datetime.timedelta(seconds=sum([video.item.length.total_seconds() for video in player.queue])))
        embed.add_field(name=f"Queue: {len(player.queue)} {cardinal('video', len(player.queue))} (total playtime: {playtime})", value="")
        for index, video in enumerate(player.queue):
            if index == 10:
                remaining = len(player.queue) - 10
                embed.add_field(name=f"... {remaining} more {cardinal('video', remaining)}", value="", inline=False)
                break
            value = f"by {video.item.author}, {views_str(video.item.views)} [{length_str(video.item.length)}]"
            embed.add_field(name=f"{index + 1}. {video.item.title}", value=value, inline=False)
    else:
        embed.add_field(name="Queue is empty", value="")

    return embed
