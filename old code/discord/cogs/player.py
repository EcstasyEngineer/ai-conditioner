import os
from discord.ext import commands
import discord

class Player(commands.cog):
    """This is a cog with commands to play music via local mp3 files or audio stream. 
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='play', aliases=['p'], description='Plays a local mp3 file or a audio stream.')
    async def play(self, ctx, *, url: str):
        """Plays a local mp3 file or a audio stream.
        
        Args:
            self
            ctx
            url (str): The url of the audio file or stream.
        """
        # Check if the user is in a voice channel
        if not ctx.author.voice:
            return await ctx.send('You are not connected to a voice channel.')
        
        # Check if the bot is in a voice channel
        if ctx.guild.voice_client is None:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.guild.voice_client.move_to(ctx.author.voice.channel)
        

        ctx.guild.voice_client.play(discord.FFmpegPCMAudio(url))
        await ctx.send(f'Now playing: {url}')

    @commands.command(name='stop', description='Stops the audio stream.')
    async def stop(self, ctx):
        """Stops the audio stream.
        
        Args:
            self
            ctx
        """
        # Check if the bot is in a voice channel
        if ctx.guild.voice_client is None:
            return await ctx.send('I am not connected to a voice channel.')
        
        ctx.guild.voice_client.stop()
        await ctx.send('Audio stream stopped.')

    @commands.command(name='pause', description='Pauses the audio stream.')
    async def pause(self, ctx):
        """Pauses the audio stream.
        
        Args:
            self
            ctx
        """
        # Check if the bot is in a voice channel
        if ctx.guild.voice_client is None:
            return await ctx.send('I am not connected to a voice channel.')
        elif ctx.guild.voice_client.is_paused():
            return await ctx.send('Audio stream is already paused.')
        else:
            ctx.guild.voice_client.pause()
            await ctx.send('Audio stream paused.')

    @commands.command(name='resume', description='Resumes the audio stream.')
    async def resume(self, ctx):
        """Resumes the audio stream.
        
        Args:
            self
            ctx
        """
        # Check if the bot is in a voice channel
        if ctx.guild.voice_client is None:
            return await ctx.send('I am not connected to a voice channel.')
        elif ctx.guild.voice_client.is_playing():
            return await ctx.send('Audio stream is already playing.')
        else:
            ctx.guild.voice_client.resume()
            await ctx.send('Audio stream resumed.')

    @commands.command(name='skip', description='Skips the current audio stream.')
    async def skip(self, ctx):
        """Skips the current audio stream.
        
        Args:
            self
            ctx
        """
        # Check if the bot is in a voice channel
        if ctx.guild.voice_client is None:
            return await ctx.send('I am not connected to a voice channel.')
        else:
            ctx.guild.voice_client.stop()

            

    @commands.command(name='queue', description='Shows the current audio stream queue.')
    async def queue(self, ctx):
        """Shows the current audio stream queue.
        
        Args:
            self
            ctx
        """
        # Check if the bot is in a voice channel
        if ctx.guild.voice_client is None:
            return await ctx.send('I am not connected to a voice channel.')
        else:
            #add url to queue
            queue.append(url)


    @commands.command(name='volume', description='Sets the volume of the audio stream.')
    async def volume(self, ctx, volume: int):
        """Sets the volume of the audio stream.
        
        Args:
            self
            ctx
            volume (int): The volume level.
        """
        pass

    @commands.command(name='loop', description='Loops the current audio stream.')
    async def loop(self, ctx):
        """Loops the current audio stream.
        
        Args:
            self
            ctx
        """
        pass

    @commands.command(name='shuffle', description='Shuffles the current audio stream queue.')
    async def shuffle(self, ctx):
        """Shuffles the current audio stream queue.
        
        Args:
            self
            ctx
        """
        pass