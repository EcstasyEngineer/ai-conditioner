from discord.ext import commands, tasks
import aiohttp


class Quote(commands.Cog):
    """This is a cog with a quote command and a quote retriever.
    Note:
        All cogs inherits from `commands.Cog`_.
        All cogs are classes.
        All cogs needs a setup function (see below).
            
    Documentation:
        https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html
    """
    def __init__(self, bot):
        self.bot = bot
        self.qod = ''#Stores the quote of the day
        self.qod_auth = ''#Stores the quote author
        self.refresh_quote.start()

    @tasks.loop(hours=1.0)
    async def refresh_quote(self):
        """Refreshes the qod and the quote author every hour.
        
        Note:
            Made due to performance optimization.
        """
        qod, author = await self.get_quote()
        self.qod = qod
        self.qod_auth = author

    async def get_quote(self):
        """Gets the quote of the day from the They Said So API.
        
        Note:
            This function uses `aiohttp` to get the quote of the day and its author.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get('https://quotes.rest/qod') as resp:
                if resp.status == 200: #Checks if the request is successfull
                    qod = (await resp.json())['contents']['quotes'][0]['quote']
                    author = (await resp.json())['contents']['quotes'][0]['author']
                    return qod, author
                else:
                    return 'Error getting the quote.', 'Unknown'

    @commands.command(name='quote', aliases=['qod',], description='Sends the quote of the day.')
    async def quote(self, ctx):
        """Sends the quote of the day in the channel where the command invoken."""
        await ctx.send(f'>>> {self.qod}    -_{self.qod_auth}_')#`>>>` is discord markup for quotes.


async def setup(bot):
    """Every cog needs a setup function like this."""
    await bot.add_cog(Quote(bot))