import discord
import json
import os
import threading
from agency_swarm import Agency, AgencyEventHandler, set_openai_key
from Agent.CEO import CEO
from Agent.AIProductManager import AIProductManager


# ✅ Ensure memory folder exists
os.makedirs("memory", exist_ok=True)

# 🧠 Per-user memory handlers
def load_threads(user_id):
    try:
        with open(f"memory/{user_id}_threads.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_threads(user_id, new_threads):
    with open(f"memory/{user_id}_threads.json", "w") as f:
        json.dump(new_threads, f)

# 🧾 Discord stream handler class
class DiscordStreamHandler(AgencyEventHandler):
    channel = None
    content = ""
    msg_obj = None

    def on_text_created(self, text):
        DiscordStreamHandler.content = text
        loop = discord_client.loop
        loop.create_task(self.send_initial_message(text))

    def on_text_delta(self, delta, snapshot):
        DiscordStreamHandler.content += delta.value  # ✅ THIS WORKS
        loop = discord_client.loop
        loop.create_task(self.edit_message(DiscordStreamHandler.content))

    async def send_initial_message(self, content):
        DiscordStreamHandler.msg_obj = await DiscordStreamHandler.channel.send(content)

    async def edit_message(self, content):
        if DiscordStreamHandler.msg_obj:
            await DiscordStreamHandler.msg_obj.edit(content=content)

# 🎮 Discord bot setup
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
discord_client = discord.Client(intents=intents)

@discord_client.event
async def on_ready():
    print(f"🤖 Logged in as {discord_client.user}")

@discord_client.event
async def on_message(message):
    if message.author == discord_client.user:
        pass

    if discord_client.user in message.mentions:
        user_id = str(message.author.id)
        prompt = message.content.replace(f"<@{discord_client.user.id}>", "").strip()

        # Set streaming target channel
        DiscordStreamHandler.channel = message.channel

        # Setup agents and agency
        ceo = CEO()
        pm = AIProductManager()

        agency = Agency(
            [ceo, pm, [ceo, pm]],
            threads_callbacks={
                "load": lambda: load_threads(user_id),
                "save": lambda new_threads: save_threads(user_id, new_threads)
            }
        )

        # ✅ Start streaming in a background thread
        threading.Thread(
            target=agency.get_completion_stream,
            args=(prompt, DiscordStreamHandler, [], ceo, "", [], None),
        ).start()


discord_client.run("MTM2Mzc5NTY0NDA4NjYyMDMxMQ.GuaTTC.LZgAW4WnTtVdlwy-UgRHCreAi-dXdnC3PYmR-E")