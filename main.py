import os
from pathlib import Path

import discord


TOKEN = os.getenv("DISCORD_TOKEN")
WELCOME_CHANNEL_ID = os.getenv("WELCOME_CHANNEL_ID")
LOGO_PATH = Path(__file__).parent / "assets" / "logo.png"

if not TOKEN:
    raise RuntimeError("Missing DISCORD_TOKEN Railway variable.")

if not WELCOME_CHANNEL_ID:
    raise RuntimeError("Missing WELCOME_CHANNEL_ID Railway variable.")

WELCOME_CHANNEL_ID = int(WELCOME_CHANNEL_ID)

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_member_join(member: discord.Member):
    channel = client.get_channel(WELCOME_CHANNEL_ID) or await client.fetch_channel(
        WELCOME_CHANNEL_ID
    )

    file = discord.File(LOGO_PATH, filename="ru-logo.png")

    embed = discord.Embed(
        title="WELCOME TO RU",
        description=(
            f"{member.mention}, welcome to the blue side.\n\n"
            "Read the rules, grab your roles, and enjoy your stay."
        ),
        color=discord.Color.from_rgb(0, 102, 255),
    )

    embed.set_author(name=member.guild.name, icon_url="attachment://ru-logo.png")
    embed.set_thumbnail(url="attachment://ru-logo.png")
    embed.add_field(
        name="Member Count",
        value=f"You are member #{member.guild.member_count}.",
        inline=True,
    )
    embed.add_field(
        name="Status",
        value="Fresh arrival",
        inline=True,
    )
    embed.set_footer(text="RU Welcome System | Electric Blue Theme")

    await channel.send(content=f"Welcome {member.mention}!", embed=embed, file=file)


client.run(TOKEN)
