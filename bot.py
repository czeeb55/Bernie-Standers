
import os
import discord
import logging
import spotipy
import asyncio
import requests
import json
from spotipy.oauth2 import SpotifyClientCredentials
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path

load_dotenv() # Load .env
#SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
#POTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)
logging.basicConfig(level=logging.DEBUG)


discordToken = os.getenv('DISCORD_BOT_TOKEN')
imgflipUsername = os.getenv('IMGFLIP_USERNAME')
imgflipSecret = os.getenv('IMGFLIP_SECRET')
imgflipURL = "https://api.imgflip.com/caption_image"
imgflipBody = {
    'template_id' : '224015000', #Bernie
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

def get_artist_song_combo(artist,song): # Needs error handling, handling for if can't find combo
    results = sp.search(q=f'artist: {artist} track: {song}', limit=1)
    items = results['tracks']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None

@bot.command(name='bernie',help='Bernie meme with Spotify link to searched Artist##Song')
async def get_song(ctx, *,args):
    if (("##" not in args)): # Checks for Artist##Song format. 
        raise discord.DiscordException("Bad Input") # Put in feedback to Discord user that the command isnt formatted properly?
    artist,song = split_input(args)
    #result = sp.search(q=f'artist: {artist}',limit=1)
    #track = result['tracks']['items'][0]['external_urls']['spotify']
    spotifySearchResults = get_artist_song_combo(artist,song)
    track = spotifySearchResults['external_urls']['spotify']
    # Need to find a way to send non-english characters. imgflip GUI supports it, but API gives blank boxes
    # May be due to how
    imgflipBody['text1'] = f"listen to {song}" 
    meme = requests.post(url=imgflipURL,data=imgflipBody)
    if(not meme.ok):
        raise discord.DiscordException(f"Failed to reach imgflip. Reason: {meme.reason}")
    elif meme.json()['success'] == False:
        raise discord.DiscordException(f"Failed to get meme from imgflip. Reason: {meme.json()['ErrorMessage']}")
    else:
        img = meme.json()['data']['url']
        await ctx.send(f"{track} {img}")
        

bot.run(discordToken)