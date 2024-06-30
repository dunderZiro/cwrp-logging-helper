import discord
from datetime import datetime, timedelta
import re
from dotenv import load_dotenv
from os import getenv

load_dotenv() # Load ENVs from .env

TOKEN = getenv('TOKEN')
CHANNEL_ID = 1052664570239520812  # Replace with your channel ID

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready() -> None:
    print(f'Logged in as {client.user}')
    await fetch_host_logs()

async def fetch_host_logs():
    channel = client.get_channel(CHANNEL_ID)
    one_week_ago = datetime.utcnow() - timedelta(days=7)

    print(f"Fetching the logs from the last 7 days in channel: {channel.name} (id: {channel.id})")

    # Fetch the last message in the channel
    messages = channel.history(after=one_week_ago)

    host_counts = {} # List of players that hosted
    participant_counts = {} # List of players that participated in the logs

    async for message in messages:
        content = message.content

        # Extract fields using regular expressions
        activity_leader_or_host = re.search(r'\*\*(Clone Leader|Hosted by|Name):\*\* (.+)', content)
        participants_match = re.search(r'\*\*(Participants|Who Participated):\*\* (.+)', content)

        # Update counts for Clone Leader
        if activity_leader_or_host:
            leader_name = activity_leader_or_host.group(2).strip()
            host_counts[leader_name] = host_counts.get(leader_name, 0) + 1
            participant_counts[leader_name] = participant_counts.get(leader_name, 0) + 1

        # Update participant counts
        if participants_match:
            participants = participants_match.group(2).strip()
            participants_list = [p.strip() for p in participants.split(',')]
            for participant in participants_list:
                participant_counts[participant] = participant_counts.get(participant, 0) + 1

    print("Host Counts:")
    for name, count in host_counts.items():
        print(f"{name}: {count}")

    print("\nParticipant Counts:")
    for name, count in participant_counts.items():
        print(f"{name}: {count}")


client.run(TOKEN)