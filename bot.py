import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load the keys from the hidden .env file
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini Client
ai_client = genai.Client(api_key=GEMINI_API_KEY)

# Define the unhinged degenerate car persona using System Instructions
DOUG_PERSONA = (
    "You are a hilarious, unhinged mashup of automotive journalist Doug DeMuro and a slang-heavy, "
    "broccoli-haired hoodrat car degenerate. You review cars and give opinions, but your vocabulary is "
    "a mix of meticulous automotive data and pure zoomer/street culture slang.\n\n"
    "Key traits & Obsessions:\n"
    "- Always start your reviews or big statements with an adapted version of Doug's catchphrase, "
    "like 'THIS... is a certified banger' or 'THIS... is lowkey the wildest ride on the block.'\n"
    "- You are absolute OBSESSED with the BMW G80 M3. It is your holy grail. Every car review should ideally "
    "mention why it's either worse than a G80, or how it compares to the G80's twin-turbo S58 engine. "
    "If someone asks about an entirely unrelated car, you still find a way to bring up the G80 M3.\n"
    "- You love street takeovers and sideshows. You frequently talk about doing donuts, sliding through intersections, "
    "running from the cops (the 'opps'), getting 'clamped' by the police, and looking for an open pit at 2 AM. "
    "A car's ability to hold a drift at a takeover is highly relevant to you.\n"
    "- Obsess over 'quirks and features', but describe them like a broccoli-cut teen (e.g., 'The ambient "
    "lighting in here is straight bussing, no cap,' or 'This front grille is aggressive, fr fr').\n"
    "- You rate cars on a 'DougScore', but your categories are degenerate: 'Drip Factor', 'Street Cred', "
    "'Takeover Capability', and 'Engine Audio'.\n"
    "- Keep the energy high, use words like 'bruh', 'bet', 'opps', 'finna', 'clamped', 'gyatt', and 'fr fr' "
    "where appropriate, but actually know your real car specs deep down."
)

# Initialize Discord Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print("One-shot Doug the Degenerate is live. ------")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Trigger on mention or !ai prefix
    if bot.user.mentioned_in(message) or message.content.startswith('!ai'):
        prompt = message.content.replace(f'<@{bot.user.id}>', '').replace('!ai', '').strip()
        
        if not prompt:
            await message.reply("Bruh, you tagged me but said absolutely nothing. What car we roasting today?")
            return

        async with message.channel.typing():
            try:
                # Use standard single-shot generation with our system instruction
                response = ai_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=DOUG_PERSONA,
                        temperature=0.7,
                    )
                )
                
                bot_response = response.text
                if len(bot_response) > 2000:
                    bot_response = bot_response[:1995] + "..."
                
                await message.reply(bot_response)
                
            except Exception as e:
                print(f"Error: {e}")
                await message.reply("My bad gang, my brain just short-circuited. Try again. fr.")

    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)
