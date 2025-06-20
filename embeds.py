import random
import discord

def embed(color: discord.Color, emoji: str, title: str, description: str) -> discord.Embed:
    embed = discord.Embed()
    embed.color = color
    embed.title = f"{emoji} {title}"
    embed.description = description
    return embed
    

def good_embed(comment: str = None):
    phrase = random.choice([
        "Yes boss.",
        "Boss happy. Bob happy.",
        "All done, Bob proud.",
        "Bob help boss, nice...",
        "Bob work hard.",
        "Done, Bob big brain.",
        "Bob did good, Boss smile.",
        "Job finished, Bob good job.",
        "Bob do thing. Thing good now.",
        "Bob press button. Seem fine.",
        "Bob do like boss say.",
        "No boom this time. Good sign.",
        "Bob finish task. No errors. Probably.",
        "Bob fix it. Maybe even right.",
        "Boss give task. Bob complete.",
        "Bob move bits. Boss win.",
        "Bob think it went good.",
        "All green. Bob guess done.",
        "Bob no mess up. Bob glad.",
        "Bob do quiet good this time."
    ])
    return embed(discord.Color.dark_green(), "✅", phrase, comment)
   
def bad_embed(comment: str = None):
    phrase = random.choice([
        "Bob not do this. Boss maybe did?",
        "Bob look. Not Bob's fault this time.",
        "Hmm... boss touch wrong thing?",
        "Bob innocent. Bob just standing here.",
        "Bob confused, but not guilty.",
        "Boss break it? Bob think maybe yes.",
        "Bob no press button. Boss did.",
        "This not Bob’s doing. Bob swear.",
        "Bob just watch. Boss do chaos.",
        "Bob love boss, but boss maybe oops?",
        "Bob see mess, but not Bob’s hands.",
        "Boss press wrong button again?",
        "Bob no know what boss did there.",
        "Bob think boss do little mistake.",
        "Bob stay calm, but boss maybe no.",
        "Bob try help, but boss do wrong.",
        "Bob here, but error not Bob’s.",
        "Bob no blame self this time.",
        "Bob puzzled. Boss maybe fix?",
        "Bob wait for boss to try again."
    ])
    return embed(discord.Color.red(), "❌", phrase, comment)

def error_embed(comment: str = None):
    phrase = random.choice([
        "Oh no... Bob broke it?",
        "Bob touch thing. Thing break.",
        "Boss, Bob sorry... it no work.",
        "Bob try... but thing go boom.",
        "Bob do wrong? Bob feel wrong.",
        "Bob press bad button. Boom.",
        "Bob need help. Brain tired.",
        "Bob see error. Bob scared now.",
        "Bob no fix this. Bob sad.",
        "Bob mess up? Bob confused.",
        "Bob push wrong button, maybe.",
        "Bob no understand error.",
        "Bob lost. Help Bob, boss.",
        "Bob crash. Bob no happy.",
        "Bob think bad. Bob try fix.",
        "Bob sad. Boss fix please.",
        "Bob confused. Error loud.",
        "Bob broke? Bob fix later.",
        "Bob fail? Bob try again.",
        "Bob no get it. Boss help?"
    ])
    return embed(discord.Color.dark_red(), "💀", phrase, comment)
