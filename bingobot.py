import discord
from bingo import Bingo
import config
import redis
import os

client = discord.Client()
bingo = Bingo()

r = redis.StrictRedis(host='localhost', port=6379, db=0)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    command = message.content.split()[0]

    handler = {
        "!bingo": bingo_handler,
        "!clearbingo": clear_bingo_handler,
        "!enablebingo": enable_bingo,
        "!disablebingo": disable_bingo,
        "!bingohelp": help_bingo,
    }.get(command, noop_handler)

    await handler(message)

    return

async def bingo_handler(message):

    enabled = r.get('bot_enabled')

    print("ENABLED: ", enabled, type(enabled))

    if enabled == b'true':
        msg = 'Here is your card {0.author.mention}!'.format(message)
        cardchannel = discord.utils.get(message.server.channels, name='bingo-cards')
        await client.send_message(cardchannel, msg)

        nick = message.author.nick or message.author.name
        uid = message.author.id

        await client.send_file(cardchannel, bingo.generate_board(nick, uid))
    else:
        await client.send_message(message.channel, "Bingo Bot is disabled at this moment, please wait for bingo night!")

    return

async def clear_bingo_handler(message):
    if message.author.id in config.moderators:
        msg = 'Starting a new Bingo round!'
        await client.send_message(message.channel, msg)
        cardchannel = discord.utils.get(message.server.channels, name='bingo-cards')
        msgs = []
        async for x in client.logs_from(cardchannel, limit=100):
            msgs.append(x)

        await client.delete_messages(msgs)

        for all_files in os.listdir('bingo_boards'):
            fpath = os.path.join('bingo_boards', all_files)
            os.unlink(fpath)

    await client.delete_message(message)
    return

async def enable_bingo(message):
    if message.author.id in config.moderators:
        msg = 'Bingo is now enabled, type `!bingo` to participate!'
        r.set('bot_enabled', 'true')
        await client.send_message(message.channel, msg)

    await client.delete_message(message)
    return

async def disable_bingo(message):
    if message.author.id in config.moderators:
        msg = 'Bingo is now disabled, see you next time!'
        r.set('bot_enabled', 'false')
        await client.send_message(message.channel, msg)

    await client.delete_message(message)
    return

async def help_bingo(message):
    msg = '**Bingo commands**\n\n'
    msg += '- `!bingo` Get a new bingo card\n'
    msg += '- `!bingohelp` This reference\n'

    if message.author.id in config.moderators:
        msg += '\n**Admin commands**\n\n'
        msg += '- `!clearbingo` Start a new round, delete all exisiting cards\n'
        msg += '- `!enablebingo` Enable the bingo card generator\n'
        msg += '- `!disablebingo` Disable the bingo card generator\n'

    await client.send_message(message.author, msg)
    await client.delete_message(message)
    return

async def noop_handler(message):
    pass

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(config.auth['token'])
