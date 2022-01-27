# ADITYA SERVER

import os
from pytgcalls import GroupCall
import ffmpeg
from config import Config
from datetime import datetime
from pyrogram import filters, Client, idle
import requests
import wget
import aiohttp
from random import randint
import aiofiles

VOICE_CHATS = {}
DEFAULT_DOWNLOAD_DIR = 'downloads/vcbot/'

api_id=Config.API_ID
api_hash=Config.API_HASH
session_name=Config.STRING_SESSION
app = Client(session_name, api_id, api_hash)

# userbot and contacts filter by dashezup's tgvc-userbot
self_or_contact_filter = filters.create(
    lambda
    _,
    __,
    message:
    (message.from_user and message.from_user.is_contact) or message.outgoing
)

# start message
@app.on_message(filters.command('start'))
async def start(client, message):
    await message.reply("🔊 Ʌɖiʈyʌ Vc Pɭɑyɘɽ Ɽʊŋŋiŋɠ ...",
                        disable_web_page_preview=True)

# ping checker
@app.on_message(filters.command('ping') & self_or_contact_filter)
async def ping(client, message):
    start = datetime.now()
    tauk = await message.reply('Pong!')
    end = datetime.now()
    m_s = (end - start).microseconds / 1000
    await tauk.edit(f'**Pong!**\n> `{m_s} ms`')

@app.on_message(filters.command('play') & self_or_contact_filter)
async def play_track(client, message):
    if not message.reply_to_message or not message.reply_to_message.audio:
        return
    input_filename = os.path.join(
        client.workdir, DEFAULT_DOWNLOAD_DIR,
        'input.raw',
    )
    audio = message.reply_to_message.audio
    audio_original = await message.reply_to_message.download()
    a = await message.reply('Ɗøwŋɭøɑɗiŋɠ...')
    ffmpeg.input(audio_original).output(
        input_filename,
        format='s16le',
        acodec='pcm_s16le',
        ac=2, ar='48k',
    ).overwrite_output().run()
    os.remove(audio_original)
    if VOICE_CHATS and message.chat.id in VOICE_CHATS:
        text = f'▶️ Pɭɑyinɠ **{audio.title}** ɧɘɽɘ ɓy Ʌɗiʈyʌ...'
    else:
        try:
            group_call = GroupCall(client, input_filename)
            await group_call.start(message.chat.id)
        except RuntimeError:
            await message.reply('Group Call doesnt exist')
            return
        VOICE_CHATS[message.chat.id] = group_call
    await a.edit(f'▶️ Pɭʌyiŋɠ **{audio.title}** ɧɘɽɘ ɓy Ʌɗiʈyʌ...')


@app.on_message(filters.command('stop') & self_or_contact_filter)
async def stop_playing(_, message):
    group_call = VOICE_CHATS[message.chat.id]
    group_call.stop_playout()
    os.remove('downloads/vcbot/input.raw')
    await message.reply('❌ Sʋƈƈɘssƒʋɭɭƴ Sʈøƥƥɘɗ Pɭʌyinɡ ❗')

    
@app.on_message(filters.command('pause') & self_or_contact_filter) 
async def pause_playing(_, message):
    group_call = VOICE_CHATS[message.chat.id]
    group_call.pause_playout() 
    os.remove('downloads/vcbot/input.raw') 
    await message.reply('Ruk gya 🤣') 
               
        
@app.on_message(filters.command('resume') & self_or_contact_filter) 
async def resume_playing(_,message) :
    group_call = VOICE_CHATS[message.chat.id]
    group_call.resume_playout() 
    os.remove('downloads/vcbot/input.raw') 
    await message.reply('Chalu ho gya ') 
    
    
@app.on_message(filters.command('join') & self_or_contact_filter)
async def join_voice_chat(client, message):
    input_filename = os.path.join(
        client.workdir, DEFAULT_DOWNLOAD_DIR,
        'input.raw',
    )
    if message.chat.id in VOICE_CHATS:
        await message.reply('✅ Ʌɭɽɘɑɗy Jøiŋɘɗ tɧɘ Vøicɘ Cʜʌt')
        return
    chat_id = message.chat.id
    try:
        group_call = GroupCall(client, input_filename)
        await group_call.start(chat_id)
    except RuntimeError:
        await message.reply('VC Øŋ kʌɽɭɘ')
        return
    VOICE_CHATS[chat_id] = group_call
    await message.reply('✅ Sʋccɘsʆʋɭɭƴ Joɩŋɘɗ tʜɘ Voɩcɘ Cʜʌt')


@app.on_message(filters.command('leave') & self_or_contact_filter)
async def leave_voice_chat(client, message):
    chat_id = message.chat.id
    group_call = VOICE_CHATS[chat_id]
    await group_call.stop()
    VOICE_CHATS.pop(chat_id, None)
    await message.reply('❎ Sʋccɘsʆʋɭɭƴ ɭɘʆt tʜɘ Voɩcɘ Cʜʌt')

app.start()
print('>>> Ʌɗiʈyʌ Vc Usɘɽɓøʈ Sʈʌɽʈɘɗ')
idle()
app.stop()
print('\n>>> Ʌɗiʈyʌ Vc Usɘɽɓøʈ Sʈøƥƥɘɗ')
