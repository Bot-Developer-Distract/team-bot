import discord
# from discord.commands import Option, View
from discord.ui import Button, View
import re
from config import BOT_TOKEN, GUILDS

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return



    # ESEA MATCHES
    if message.content.startswith('.esea'):
        organiser_id = message.author.id
        players = []
        msg_items = message.content.split(' ')
        msg_items.pop(0)
        msg = " ".join(msg_items)
        url = re.search(r'(https?://[^\s]+)', msg)
        esea_url = re.search(r'(https?://play.esea.net[^\s]+)', msg)

        if msg:
            if esea_url:
                bot_msg = f'[ESEA] Can you play? See {url.group(0)} for details.'
            elif url and not esea_url:
                bot_msg = f'Please specify a valid ESEA link'            
            else:
                bot_msg = f'[ESEA] Can you play an ESEA match on {msg}?'
            
        else:
            await message.channel.send(f"Please specify either a match url or propose a date and time.")


        async def button_y_cb(interaction):
            msg = interaction.message.content
            msg_id = interaction.message.jump_url
            new_msg = ''
            player_yes_id = interaction.user.id
            player_yes_name = interaction.user.name

            if player_yes_name in players:
                await message.channel.send(f"<@{player_yes_id}> You have already accepted.")
            else:
                players.append(player_yes_name)
                # await interaction.response.send_message(f"{player_yes} accepted.")
                if new_msg:
                    new_msg = f'{new_msg} \n✅ <@{player_yes_id}> accepted.'
                else:
                    new_msg = f'{msg} \n✅ <@{player_yes_id}> accepted.'
                await interaction.message.edit(content=new_msg)
                
                notify_organiser = f'<@{organiser_id}> **{player_yes_name}** has accepted the match. {msg_id}'
                await message.channel.send(content=notify_organiser)

        async def button_n_cb(interaction):
            msg = interaction.message.content
            msg_id = interaction.message.jump_url
            new_msg = ''
            player_yes_id = interaction.user.id
            player_yes_name = interaction.user.name

            if player_yes_name in players:
                for idx, name in enumerate(players):
                    if player_yes_name == name:
                        players.pop(idx)

                # await interaction.response.send_message(f"{player_yes} accepted.")
                if new_msg:
                    new_msg = f'{new_msg} \n❌ <@{player_yes_id}> declined.'
                else:
                    new_msg = f'{msg} \n❌ <@{player_yes_id}> declined.'
                await interaction.message.edit(content=new_msg)
                
                notify_organiser = f'<@{organiser_id}> **{player_yes_name}** has declined the match. {msg_id}'
                await message.channel.send(content=notify_organiser)
        
        # Create buttons
        button_y = Button(label="YES", style=discord.ButtonStyle.success)
        button_y.callback = button_y_cb

        button_n = Button(label="NO", style=discord.ButtonStyle.danger)
        button_n.callback = button_n_cb
        
        # Create View
        view = View()
        view.add_item(button_y)
        view.add_item(button_n)
        
        if msg and url and not esea_url:
            await message.channel.send(bot_msg)
        elif msg:
            await message.channel.send(bot_msg, view=view)


bot.run(BOT_TOKEN)
