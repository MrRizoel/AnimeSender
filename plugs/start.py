
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden

from database import users
from . import START_MSG, START_BUTTONS, UPLOAD_CHANNEL, CHANNEL, BOT_USERNAME


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
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("• Join Channel •", url=link)]
                    ])
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
      except Exception:
         try:
            await wait_message.edit_text("Something went wrong..!")
         except Exception:
            await wait_message.delete()
            await message.reply_text("Something went wrong..!")
         return
      anime_text = anime.text
      anime_caption = anime_text.format(anime.video.duration, anime.video.file_size)
      anime_buttons = [[(InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL}")]]
      await RiZoeL.send_video(chat.id, UPLOAD_CHANNEL, anime.id, caption=anime_caption, reply_markup=InlineKeyboardMarkup(anime_buttons))

   else:
       await RiZoeL.send_message(START_MSG.format(user.mention), reply_markup=InlineKeyboardMarkup(START_BUTTONS))

   print(f"Started by {user.first_name}!")
