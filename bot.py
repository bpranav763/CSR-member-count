import discord
import requests
import asyncio

# --- CONFIG ---
TOKEN = 'MTM5ODYwODU0MTMyOTM5MTY5OA.G0F9Eg.4s7DH2fIXlonZddPiIWsAIhIMGizUMe6_JHSX8'           # Your Discord Bot Token
CHANNEL_ID = 1432784489167454359            # Replace with your channel or thread ID (int, not string)
GROUP_ID = '1003228779'  # Replace with your Roblox group ID
UPDATE_INTERVAL = 300              # Seconds between checks (e.g. 300 = every 5 minutes)

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def get_member_count(group_id):
    url = f"https://groups.roblox.com/v1/groups/{group_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("memberCount", "Error")
    return "Error"

async def update_message_loop():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print("ERROR: Channel not found.")
        return

    # Send the initial message and save the message ID
    message = await channel.send(f"Current Roblox Group Member Count: ...")
    last_count = None
    while True:
        count = await get_member_count(GROUP_ID)
        if count != last_count:
            await message.edit(content=f"Current Roblox Group Member Count: {count}")
            last_count = count
        await asyncio.sleep(UPDATE_INTERVAL)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    client.loop.create_task(update_message_loop())

client.run(TOKEN)
