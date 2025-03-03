from discord.ext import commands
import discord
import datetime


class Tools(commands.Cog):
    """This is a cog with simple and useful commands.
	Note:
		All cogs inherits from `commands.Cog`_.
		All cogs are classes, so they need self as first argument in their methods.
		All cogs use different decorators for commands and events (see example in dev.py).
		All cogs needs a setup function (see below).
    
    Documentation:
        https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html
    """
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='echo')
    async def echo(self, ctx, *, message):
        """This command outputs the string that is being passed as argument.

        Args:
            self
            ctx 
            *, message (this sets the 'consume rest' behaviour for arguments)
        """
        await ctx.message.delete()
        await ctx.send(message)


    @commands.command(name='ping')
    async def ping(self, ctx):
        """Sends a message with bot's latency in ms in the channel where the command has been invoked.
		
		Note:
			`bot.latency` outputs the latency in seconds.
		"""
        await ctx.send(f'🏓 {round(self.bot.latency * 1000)} ms.')


    @commands.command(name='info')
    async def get_info(self, ctx):
        """This coroutine sends an embedded message with some info.
		
		Documentation:
			https://discordpy.readthedocs.io/en/latest/api.html#discord.Embed
		"""
		#embed example
        embed = discord.Embed(
            title = 'Info',
            description = 'An info message using an embed!',
            colour = discord.Colour.blurple(), #0x7289da
			timestamp = datetime.datetime.utcnow()
        )
		#embed fields
        embed.set_footer(text=f'this bot is running on {len(self.bot.guilds)}')
        embed.add_field(name='Version', value='0.1', inline=True)
        embed.add_field(name='Language', value='Python 3.8', inline=True)
        embed.set_author(name='nect', url='https://gist.github.com/bynect', icon_url='http://tiny.cc/nect-user-pic')
        
        await ctx.send(embed = embed)

		
async def setup(bot):
    """Every cog needs a setup function like this."""
    await bot.add_cog(Tools(bot))
    