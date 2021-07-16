
import os
import discord
import logging
import spotipy
#import asyncio
import requests
#import json
#import dicttoxml
import pprint
from spotipy.oauth2 import SpotifyClientCredentials
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path

load_dotenv() # Load .env
logging.basicConfig(level=logging.INFO)
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
try:
    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)  
except:
    raise("Can't auth to spotify")


discordToken = os.getenv('DISCORD_BOT_TOKEN')
imgflipUsername = os.getenv('IMGFLIP_USERNAME')
imgflipSecret = os.getenv('IMGFLIP_SECRET')
imgflipURL = "https://api.imgflip.com/caption_image"
imgflipBody = {
    'template_id' : '224015000',
    'username' : imgflipUsername,
    'password' : imgflipSecret,
    'text0' : 'I am once again asking you to',
    'text1' : 'listen to H.E.R.'
}

# Bot will only respond to commands with this prefix
bot = commands.Bot(command_prefix="$", case_insensitive=True)

def split_input(input):
    #combinedInput = " ".join(str(input))
    artist,song = input.split("##")
    artist = artist.strip() # Remove trailing/leading whitespace
    song = song.strip()
    return artist,song

def validate_input(input):
    if "##" not in input:
        return "Invalid"
    else:
        splitInput = input.split("\n")
        for line in splitInput:
            if "##" not in line:
                continue
            else:
                return line


def get_artist_song_combo(artist,song):
    results = sp.search(q=f'artist: {artist} track: {song}', limit=1)
    items = results['tracks']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None

# Check for "English" characters until find a way to send non-English to imgflip
# Will still have issues if the name is in unsupported characters but this'll take care of most scenarios for now
def is_english(s):
    try:
         s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True
@bot.command(name='tornado',help='🌪🌪🌪🌪🌪🌪🌪🌪🌪🌪🌪🌪🌪🌪🌪🌪BBBYYYYYYEEEEEEEEEEEEEEEEEEE🌪🌪🌪🌪🌪🌪🌪🌪🌪🌪🌪🌪🌪🌪🌪🌪')
async def post_ariana_tornado(ctx):
    if ctx.message.author == bot.user:
        return
    else:
        await ctx.message.channel.send('🌪🌪🌪🌪🌪🌪🌪🌪🌪🌪🌪🌪🌪🌪🌪🌪\nhttps://www.youtube.com/watch?v=pZKzRK9tStY\n🌪🌪🌪🌪🌪🌪🌪🌪🌪🌪🌪🌪🌪🌪🌪🌪')

@bot.command(name='no',help='Bernie finger wags at you')
async def finger_wag(ctx):
    if ctx.message.author == bot.user:
        return
    else:
        await ctx.message.channel.send('https://tenor.com/view/berniesanders-gif-5932778')

@bot.command(name='yes',help='Bernie finger wags at you')
async def finger_wag(ctx):
    if ctx.message.author == bot.user:
        return
    else:
        await ctx.message.channel.send('https://tenor.com/view/bernie-yes-finger-point-gif-13458091')

@bot.command(name='work',help='work work DEPRESSSIIIOOONNNNNN')
async def anxiety(ctx):
    if ctx.message.author == bot.user:
        return
    else:
        await ctx.message.channel.send('https://cdn.discordapp.com/attachments/810287917242646538/849450349131726887/video0.mp4')
@bot.command(name='june',help='if you do mouth stuff, you get 4')
async def anxiety(ctx):
    if ctx.message.author == bot.user:
        return
    else:
        await ctx.message.channel.send('https://cdn.discordapp.com/attachments/845801615781003275/862088022929571860/video0.mp4')


@bot.command(name='bernie',help='Bernie meme with Spotify link to searched Artist##Song\nInput: Artist ## Song\nex: Reol ## 1LDK')
async def get_song(ctx, *,args):
    result = validate_input(args)
    if result == "Invalid": # Checks for Artist##Song format. 
        if ctx.message.author == bot.user:
            return
        else:
            await ctx.message.channel.send('I am once again asking you to use the Artist ## Song syntax. Ex: Reol ## 1LDK')
        raise discord.DiscordException("Improper syntax")
    else:
        artist,song = split_input(result)
    
    spotifySearchResults = get_artist_song_combo(artist,song)

    if spotifySearchResults == None:
        if ctx.message.author == bot.user:
            return
        else:
            await ctx.message.channel.send('Could not find a match on Spotify\nI am once again asking you to check your syntax and give me a valid artist ## song.')
        raise discord.DiscordException(f"Could not find a result for artist ## song combo.\nSearched for Artist:{artist},Song:{song}")
    else:
        track = spotifySearchResults['external_urls']['spotify']
        trackName = spotifySearchResults['name'] # Will have later steps use the full song name if someone does a partial song name search
    # Need to find a way to send non-english characters. imgflip GUI supports it, but API gives blank boxes
    # May be due to encoding?
    #song = song.encode('utf-8')
    #headers = {"Content-Type": "text/html; charset=UTF-8"}
    
    if is_english(trackName):
        imgflipBody['text1'] = f"listen to {trackName}"
    else:
        imgflipBody['text1'] = f"listen to {artist}"
    meme = requests.post(url=imgflipURL,data=imgflipBody)
    if(not meme.ok):
        raise discord.DiscordException(f"Failed to reach imgflip. Reason: {meme.reason}")
    elif meme.json()['success'] == False:
        raise discord.DiscordException(f"Failed to get meme from imgflip. Reason: {meme.json()['error_message']}")
    else:
        img = meme.json()['data']['url']
        await ctx.send(f"{track} {img}")
        
@bot.event
async def on_message(message):
    if (("get a server" in message.content.lower()) or ("bernie at work" in message.content.lower()) or ("bernie is at work" in message.content.lower())) and (message.author.name.lower() == "swizzlekat"):
        imgflipBody['text1']="mind ya business"
        meme = requests.post(url=imgflipURL,data=imgflipBody)
        if(not meme.ok):
            raise discord.DiscordException(f"Failed to reach imgflip. Reason: {meme.reason}")
        elif meme.json()['success'] == False:
            raise discord.DiscordException(f"Failed to get meme from imgflip. Reason: {meme.json()['error_message']}")
        else:
            img = meme.json()['data']['url']
            await message.channel.send(f"{message.author.mention} {img}")
    elif "get a server" in message.content.lower():
        await message.channel.send(f"{message.author.mention}https://tenor.com/view/im-watching-watch-you-eyes-on-you-kid-cute-gif-16282723")
    await bot.process_commands(message)
bot.run(discordToken)