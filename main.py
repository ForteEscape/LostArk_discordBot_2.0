import discord
import pandas as pd
from discord.ext import commands

path = "data/token.txt"
token_df = pd.read_csv(path)
bot_execute_flag = False


class CustomBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents=discord.Intents.all(),
            sync_command=True,
            # application_id=861973692292005908
            application_id=863060411414216724             # test_service
        )
        self.initial_extensions = ['Cogs.PlayerContentHandler',
                                   'Cogs.EmojiHandler', 'Cogs.MarketHandler',
                                   'Cogs.PartyHandler','Cogs.RefiningHandler']

    async def setup_hook(self):
        for ext in self.initial_extensions:
            await self.load_extension(ext)
        await bot.tree.sync(
            # guild=discord.Object(id=827887392047497216)
            guild=discord.Object(id=863529285553618944)     # test_service
        )

    async def on_ready(self):
        print("login")
        print(self.user.name)
        print(self.user.id)
        await self.change_presence(status=discord.Status.online)


if not bot_execute_flag:
    token = token_df.loc[token_df['Bot'] == 'LOA_BOT_BETA', 'Token'][0]
else:
    token = token_df.loc[token_df['Bot'] == 'LOA_BOT', 'Token'][1]

bot = CustomBot()
bot.run(token)
