import asyncio
import base64
import json
import os

import discord
import redis

global client, player_count
player_count = None

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")

def redis_handler(message):
    global player_count
    global client

    data = json.loads(base64.b64decode(json.loads(message['data'])['Data']).decode('ascii'))
    print(data)
    if "ServerType" in data and data["ServerType"] == 3:
        print(f"Updating player count if changed")
        if 'Online' in data and data['Online'] != player_count:
            player_count = data['Online']
            print(f"Updating online count to {player_count}")
            asyncio.run(client.change_presence(activity=discord.Game(name=f"{player_count} users online")))

r = redis.Redis(host='localhost', port=6379, db=0)
p = r.pubsub(ignore_subscribe_messages=True)
p.subscribe(**{'messages': redis_handler})
p.run_in_thread(sleep_time=0.001)

client.run(os.getenv('DISCORD_TOKEN'))
