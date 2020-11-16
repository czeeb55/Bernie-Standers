
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
logging.basicConfig(level=logging.INFO)


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

bot = commands.Bot(command_prefix="-")

@bot.command(name='GetSong',help='Gets a song from Spotify')
async def get_song(ctx, song):
    result = sp.search(q=f'track: {song}', type='track',limit=1)
    track = result['tracks']['items'][0]['external_urls']['spotify']
    imgflipBody['text1'] = f"listen to {song}"
    meme = requests.post(url=imgflipURL,params=imgflipBody)
    if(not meme.ok):
        print("Oopsy")
        return
    img = meme.json()['data']['url']
    await ctx.send(f"{track} {img}")
        

bot.run(discordToken)