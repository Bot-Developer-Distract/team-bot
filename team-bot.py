import discord
# from discord.commands import Option, View
from discord.ui import Button, View
import re
from config import BOT_TOKEN, GUILDS

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


def handle_response(d, id, response):
    if id in d and d[id] != response:
        # Update the player response
        d[id] = response
        print(f'Player response updated to {response}')
    elif not id in d:
        # Add the player response
        d[id] = response
        print('Player response added')
    else: 
        # Do nothing
        print('Nothing to do!')

def build_message(message, d):
    msg_list = [message]

    for id in d:
        if d[id] == 'accepted':
            emoji = '✅'
        elif d[id] == 'declined':
            emoji = '❌'
        msg_list.append(f"{emoji}<@{id}> has {d[id]}")

    updated_msg = '\n'.join(msg_list)
    print(updated_msg)

    return updated_msg
    
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    triggers = ('.csgo')

    if message.content.startswith(triggers):

        organiser_id = message.author.id
        players = {}
        msg_items = message.content.split(' ')
        msg_items.pop(0)
        organiser_msg = " ".join(msg_items)
        url = re.search(r'(https?://[^\s]+)', organiser_msg)
        esea_url = re.search(r'(https?://play.esea.net[^\s]+)', organiser_msg)

        async def btn_accept_cb(interaction):
            responder_id = interaction.user.id
            handle_response(players, responder_id, 'accepted')
            await interaction.message.edit(content=build_message(bot_msg, players))
            print(players)

        async def btn_decline_cb(interaction):
            responder_id = interaction.user.id
            handle_response(players, responder_id, 'declined')
            await interaction.message.edit(content=build_message(bot_msg, players))
            print(players)

        # Create buttons
        btn_accept = Button(label="ACCEPT", style=discord.ButtonStyle.success)
        btn_accept.callback = btn_accept_cb

        btn_decline = Button(label="DECLINE", style=discord.ButtonStyle.danger)
        btn_decline.callback = btn_decline_cb
        
        # Create View
        view = View(timeout=None)
        view.add_item(btn_accept)
        view.add_item(btn_decline)

        # Construct message
        bot_msg = f"<@886645793031860234> <@{organiser_id}> has requested players. *[Request: {organiser_msg}]*"
        
        if organiser_msg:
            await message.channel.send(bot_msg, view=view)
        else:
            await message.channel.send("Please add your request!")


bot.run(BOT_TOKEN)
