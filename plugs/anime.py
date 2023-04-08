
import time, datetime, asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import ChatAdminRequired
from . import DEVS, UPLOAD_CHANNEL, CHANNEL, BOT_USERNAME, encode
from database import users 

def get_time(seconds: int) -> str:
    count = 0
    real_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    hmm = len(time_list)
    for x in range(hmm):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        real_time += time_list.pop() + ", "
    time_list.reverse()
    real_time += ":".join(time_list)
    return real_time

def get_file_size(file_size):
    size = file_size/1024

    if size <= 1024:
        return str(round(size,3)) + " kb"
    elif size > 1024:
        size = size/1024
        if size <= 1024:
            return str(round(size,3)) + " mb"
        elif size > 1024:
            size = size/1024
            return str(round(size,3)) + " gb"

blue_print = """
**Anime Twilight!**

**• Name:** {}
**• Duration:** {}
**• File Size:** {}
"""

@Client.on_message(filters.user(DEVS) & filters.command(["set", "setanime", "anime"]))
async def setanime(RiZoeL: Client, message: Message):
   args = "".join(message.text.split(maxsplit=1)[1:]).split(" ", 1)
   replied = message.reply_to_message
   if (replied and replied.photo):
      if len(args) == 2:
         msg_id = int(args[0])
         anime_name = str(args[1])
         try:
            anime = await RiZoeL.get_messages(UPLOAD_CHANNEL, msg_id)
         except ChatAdminRequired:
            await message.reply("I'm not admin in {}!").format(UPLOAD_CHANNEL)
            return
         multiple = int(int(msg_id) * 1517994352)
         message_string = await encode(f"anime-{multiple}")
         anime_caption = blue_print.format(anime_name, get_time(anime.video.duration), get_file_size(anime.video.file_size))
         buttons = [[(InlineKeyboardButton("Watch Now 🎬", url=f"https://t.me/{BOT_USERNAME}?start={message_string}"))]]
         x = await RiZoeL.send_photo(
                      CHANNEL,
                      replied.photo.file_id,
                      caption=anime_caption,
                      reply_markup=InlineKeyboardMarkup(buttons),
                      )
         await message.reply(f"Your Anime uploaded! [Click here](https://t.me/{CHANNEL}/{x.id})", disable_web_page_preview=True)
         data = users.get_all_users()
         for db in data:
            try:
               await RiZoeL.send_message(db.user_id, text=f"**New Anime uploaded! [Click here.](https://t.me/{CHANNEL}/{x.id})**", disable_web_page_preview=True)
               await asyncio.sleep(1)
            except Exception as a:
               print(a)
      else:
         await message.reply("Wrong Usage!")
   else:
      await message.reply("Reply to picture!")
