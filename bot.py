
import os
import discord
import logging
import spotipy
import asyncio
import requests
import json
import dicttoxml
import pprint
from spotipy.oauth2 import SpotifyClientCredentials
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path

load_dotenv() # Load .env
logging.basicConfig(level=logging.DEBUG)
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
bot = commands.Bot(command_prefix="$")

def split_input(input):
    #combinedInput = " ".join(str(input))
    artist,song = input.split("##")
    artist = artist.strip() # Remove trailing/leading whitespace
    song = song.strip()
    return artist,song

def get_artist_song_combo(artist,song):
    results = sp.search(q=f'artist: {artist} track: {song}', limit=1)
    items = results['tracks']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None

# Check for "English" characters until find a way to send non-English to imgflip
def is_english(s):
    try:
         s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

@bot.command(name='bernie',help='Bernie meme with Spotify link to searched Artist##Song')
async def get_song(ctx, *,args):
    if (("##" not in args)): # Checks for Artist##Song format. 
        if ctx.message.author == bot.user:
            return
        else:
            await ctx.message.channel.send('I am once again asking you to check your syntax and give me a valid artist ## song. Please try again')
        raise discord.DiscordException("Improper syntax")

    artist,song = split_input(args)
    spotifySearchResults = get_artist_song_combo(artist,song)

    if spotifySearchResults == None:
        if ctx.message.author == bot.user:
            return
        else:
            await ctx.message.channel.send('I am once again asking you to check your syntax and give me a valid artist ## song. Please try again')
        raise discord.DiscordException("Could not find a result for artist ## song combo")
    else:
        track = spotifySearchResults['external_urls']['spotify']
    # Need to find a way to send non-english characters. imgflip GUI supports it, but API gives blank boxes
    # May be due to encoding?
    #song = song.encode('utf-8')
    #headers = {"Content-Type": "text/html; charset=UTF-8"}

    if is_english(song):
        imgflipBody['text1'] = f"listen to {song}"
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
        

bot.run(discordToken)