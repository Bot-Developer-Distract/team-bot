import discord
from discord.ext import commands
from config import BOT_TOKEN


def handle_response(message_content, user_id, response=''):
    msg_list = message_content.split('\n')
    responded = False

    if response == 'accepted':
        emoji = '✅'
    elif response == 'declined':
        emoji = '❌'

    for idx, val in enumerate(msg_list[2:], 2):
        if str(user_id) in val:
            msg_list[idx] = f"{emoji}<@{user_id}> has {response}"
            responded = True

    if not responded:
        msg_list.append(f"{emoji}<@{user_id}> has {response}")

    return '\n'.join(msg_list)

class PersistentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        print(f'Initialised {self.id}')

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.success, custom_id="persistent_view:accept")
    async def btn_accept_cb(self, button: discord.ui.Button, interaction: discord.Interaction):
        message_content = handle_response(interaction.message.content, interaction.user.id, response='accepted')
        await interaction.message.edit(content=message_content)

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.danger, custom_id="persistent_view:decline")
    async def btn_decline_cb(self, button: discord.ui.Button, interaction: discord.Interaction):
        message_content = handle_response(interaction.message.content, interaction.user.id, response='declined')
        await interaction.message.edit(content=message_content)

class PersistentViewBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or("$"))
        self.persistent_views_added = False

    async def on_ready(self):
        if not self.persistent_views_added:
            self.add_view(PersistentView())
            self.persistent_views_added = True
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")


bot = PersistentViewBot()

@bot.command()
@commands.is_owner()
async def prepare(ctx: commands.Context):
    await ctx.send("What's your favourite colour?", view=PersistentView())

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('.csgo'):

        organiser_id = message.author.id
        msg_items = message.content.split(' ')
        msg_items.pop(0)
        organiser_msg = " ".join(msg_items)

        bot_msg = f"<@886645793031860234> <@{organiser_id}> has requested players for **CSGO**.\n*[Request: {organiser_msg}]*"

        await message.channel.send(bot_msg, view=PersistentView())

bot.run(BOT_TOKEN)