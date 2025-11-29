import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

def load_all_extensions(bot):
    folders = ["commands", "events", "utils", "ui"]
    for folder in folders:
        for file in os.listdir(folder):
            if file.endswith(".py") and file != "__init__.py":
                ext_path = f"{folder}.{file[:-3]}"
                try:
                    bot.load_extension(ext_path)
                    print(f"[+] Loaded {ext_path}")
                except Exception as e:
                    print(f"[-] Failed {ext_path}: {e}")

@bot.event
async def on_ready():
    print(f"✅ Online as {bot.user} | ID: {bot.user.id}")

if __name__ == "__main__":
    load_all_extensions(bot)
    bot.run(TOKEN)
