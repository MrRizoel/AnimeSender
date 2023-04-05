
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden

from database import users
from . import UPLOAD_CHANNEL, CHANNEL, BOT_USERNAME

START_MSG = """
**Hue Hue {}** it Anime Twilight Bot

  • I can provide to latest animes 😉 simply join my channel and start me using upload/watch now buttons!

**Powered by @TeamRed7|| click below button!**
"""

START_PIC = "https://telegra.ph//file/803de524cec0035d7f64f.jpg"

CHANNEL_BUTTON = [[(InlineKeyboardButton("Anime Twilight ✨", url=f"https://t.me/{CHANNEL}"))]]


@Client.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channels(RiZoeL: Client, msg: Message):   
    if not CHANNEL:
        return
    try:
        try:
            await RiZoeL.get_chat_member(CHANNEL, msg.from_user.id)
        except UserNotParticipant:
            if MUST_JOIN.isalpha():
                link = "https://t.me/" + CHANNEL
            else:
                chat_info = await RiZoeL.get_chat(CHANNEL)
                link = chat_info.invite_link
            try:
                await msg.reply(
                    f"You must join [this channel]({link}) to use me. After joining try again !",
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup(CHANNEL_BUTTON),
                )
                await msg.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        print(f"I'm not admin in the CHANNEL chat : {CHANNEL} !")

 
@Client.on_message(filters.private & filters.command("start"))
async def start(RiZoeL: Client, message: Message):
   chat = message.chat
   user = message.from_user
   users.adduser(user.id)
   text = message.text

   if len(text)>7:
      wait_message = await message.reply("Please wait...")
      anime_option = text.split(" ", 1)[1]
      argument = anime_option.split("-")
      try:
         anime = await RiZoeL.get_messages(UPLOAD_CHANNEL, int(argument[1]))
      except Exception as er:
         print(str(er))
         try:
            await wait_message.edit_text("Something went wrong..!")
         except Exception:
            await wait_message.delete()
            await message.reply_text("Something went wrong..!")
         return
      if anime.text:
         anime_caption = str(anime.text)
      else:
         anime_caption = "**Here is you anime!**"
      await RiZoeL.copy_message(chat.id, UPLOAD_CHANNEL, anime.id, caption=anime_caption, reply_markup=InlineKeyboardMarkup(CHANNEL_BUTTON))

   else:
       await RiZoeL.send_photo(chat.id, START_PIC, caption=START_MSG.format(user.mention), reply_markup=InlineKeyboardMarkup(CHANNEL_BUTTON))

   print(f"Started by {user.first_name}!")
