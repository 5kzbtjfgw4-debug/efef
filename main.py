import os

import discord


TOKEN = os.getenv("DISCORD_TOKEN")
WELCOME_CHANNEL_ID = os.getenv("WELCOME_CHANNEL_ID")
LEGIT_CHECK_CHANNEL_ID = 1487548489130053795
RESTOCK_CHANNEL_ID = 1511862391795876060

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

    message = (
        "👋 Hello! Welcome to Resellus! Check out "
        f"<#{LEGIT_CHECK_CHANNEL_ID}> & <#{RESTOCK_CHANNEL_ID}> "
        "to learn more about our store & community — we’re happy to see you! 🎉"
    )

    await channel.send(message)


client.run(TOKEN)
