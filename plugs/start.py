import re
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden
from pyrogram.enums import ChatMemberStatus

from database import users
from . import UPLOAD_CHANNEL, CHANNEL, BOT_USERNAME, decode, DEVS

START_MSG = """
**Hue Hue {}** it Anime Twilight Bot

  • I can provide to latest animes 😉 simply join my channel and start me using upload/watch now buttons!

**Powered by @TeamRed7|| click below button!**
"""

START_PIC = "https://telegra.ph//file/803de524cec0035d7f64f.jpg"

CHANNEL_BUTTON = [[(InlineKeyboardButton("Anime Twilight ✨", url=f"https://t.me/{CHANNEL}"))]]

async def check_sub(RiZoeL, update):
    if not CHANNEL:
        return True
    user_id = update.from_user.id
    if user_id in DEVS:
        return True
    try:
        member = await RiZoeL.get_chat_member(CHANNEL, user_id=user_id)
    except UserNotParticipant:
        return False
    except ChatAdminRequired:
        print(f"I'm not admin in the CHANNEL chat : {CHANNEL} !")
        return True
    except ChatWriteForbidden:
        return True

    if not member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
        return False
    else:
        return True


async def join_message(RiZoeL: Client, message: Message):
    if len(message.text)>7:
      buttons = [
                [
                 InlineKeyboardButton("Anime Twilight ✨", url=f"https://t.me/{CHANNEL}")
                ], [
                 InlineKeyboardButton("- Try Again -",url = f"https://t.me/{BOT_USERNAME}?start={message.command[1]}")
                ], ]
    else:
      buttons = CHANNEL_BUTTON

    await message.reply(
        f"You must join [this channel](https://t.me/{CHANNEL}) to use me. After joining try again !",
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        disable_web_page_preview=True
    )


@Client.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channels(RiZoeL: Client, message: Message):   
    if not CHANNEL:
        return
    text = message.text
    if re.search("start".lower(), text.lower()):
      return
    if not await check_sub(RiZoeL, message):
      await message.reply(
        f"You must join [this channel](https://t.me/{CHANNEL}) to use me. After joining try again !",
        reply_markup=InlineKeyboardMarkup(CHANNEL_BUTTON),
        quote=True,
        disable_web_page_preview=True
      )
      await message.stop_propagation()


@Client.on_message(filters.private & filters.command("start"))
async def start(RiZoeL: Client, message: Message):
   chat = message.chat
   user = message.from_user
   users.adduser(user.id)
   text = message.text
   if await check_sub(RiZoeL, message):
      pass
   else:
      await join_message(RiZoeL, message)
      return 

   if len(text)>7:
      try:
          base64_string = text.split(" ", 1)[1]
      except:
          return
      string = await decode(base64_string)
      argument = string.split("-")
      wait_message = await message.reply("please wait!....")
      try:
         try:
            msg_id = int(int(argument[1]) / 1517994352)
         except:
            return
         anime = await RiZoeL.get_messages(UPLOAD_CHANNEL, msg_id)
      except Exception as er:
         print(str(er))
         try:
            await wait_message.edit_text("Something went wrong..!")
         except Exception:
            await wait_message.delete()
            await message.reply_text("Something went wrong..!")
         return
      try:
         anime_caption = "" if not anime.caption else anime.caption.html
      except Exception:
         anime_caption = "**Here is you anime!**"
      await RiZoeL.copy_message(chat.id, UPLOAD_CHANNEL, anime.id, caption=anime_caption, reply_markup=InlineKeyboardMarkup(CHANNEL_BUTTON))
      await wait_message.delete()

   else:
       await RiZoeL.send_photo(chat.id, START_PIC, caption=START_MSG.format(user.mention), reply_markup=InlineKeyboardMarkup(CHANNEL_BUTTON))

   print(f"Started by {user.first_name}!")

