import discord.ui
import discord


class TestView(discord.ui.View):
    async def on_timeout(self) -> None:
        # Step 2
        for item in self.children:
            item.disabled = True

        # Step 3
        await self.message.edit(view=self)

    @discord.ui.button(label='Example')
    async def example_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Hello!', ephemeral=True)