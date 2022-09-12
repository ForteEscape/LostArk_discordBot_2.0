from discord import app_commands
from discord.ext import commands
from discord import Interaction
from discord import Object


class Test(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="test")
    async def test(self, interaction: Interaction) -> None:
        await interaction.response.send_message("testing")


async def setup(bot: commands.Bot):
    await bot.add_cog(
        Test(bot),
        guilds=[Object(id=863529285553618944)]
    )