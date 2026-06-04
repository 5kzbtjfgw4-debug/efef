import os

import discord
from discord.ext import commands


TOKEN = os.getenv("DISCORD_TOKEN")
WELCOME_CHANNEL_ID = os.getenv("WELCOME_CHANNEL_ID")

if not TOKEN:
    raise RuntimeError("Missing DISCORD_TOKEN Railway variable.")

if not WELCOME_CHANNEL_ID:
    raise RuntimeError("Missing WELCOME_CHANNEL_ID Railway variable.")

WELCOME_CHANNEL_ID = int(WELCOME_CHANNEL_ID)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.event
async def on_member_join(member: discord.Member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID) or await bot.fetch_channel(WELCOME_CHANNEL_ID)

    embed = discord.Embed(
        title="Welcome to the Server",
        description=(
            f"Welcome {member.mention}!\n\n"
            "We are glad to have you here. Check the rules, grab your roles, "
            "and enjoy your stay."
        ),
        color=discord.Color.from_rgb(88, 101, 242),
    )

    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(
        name="Member Count",
        value=f"You are member #{member.guild.member_count}.",
        inline=False,
    )
    embed.set_footer(text=f"Welcome to {member.guild.name}")

    await channel.send(embed=embed)


bot.run(TOKEN)
