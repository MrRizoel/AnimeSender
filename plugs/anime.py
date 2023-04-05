
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import ChatAdminRequired
from . import DEVS, UPLOAD_CHANNEL, CHANNEL, BOT_USERNAME


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
         anime_caption = blue_print.format(anime_name, anime.video.duration, anime.video.file_size)
         buttons = [[(InlineKeyboardButton("Watch Now 🎬", url=f"https://t.me/{BOT_USERNAME}?start=anime={msg_id}"))]]
         x = await RiZoeL.send_photo(
                      CHANNEL,
                      replied.photo.file_id,
                      caption=anime_caption,
                      reply_markup=InlineKeyboardMarkup(buttons),
                      )
         await message.reply(f"Your Anime uploaded! [Click here](https://t.me/{CHANNEL}/{x.id})", disable_web_page_preview=True)
      else:
         await message.reply("Wrong Usage!")
   else:
      await message.reply("Reply to picture!")
