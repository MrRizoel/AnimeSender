
import datetime 
from pyrogram import filters, Client as RiZoeL
from pyrogram.types import Message
from . import DEVS
from database import users

@RiZoeL.on_message(filters.user(DEVS) & filters.private & filters.command(["ping", "speed"]))
async def pong(_, message: Message):   
   start = datetime.datetime.now()
   end = datetime.datetime.now()
   ms = (end-start).microseconds / 1000
   await message.reply(f"**PONG:** {ms}ms")

@RiZoeL.on_message(filters.user(DEVS) & filters.private & filters.command(["stats", "stat", "users"]))
async def status(_, message: Message):   
   x = await message.reply("fetching stats....")
   await x.edit_text(f"**Total Users in bot:** `{users.count()}`")

@RiZoeL.on_message(filters.user(DEVS) & filters.command(["broadcast", "gcast"]))
async def gcast_(_, e: Message):
    txt = ' '.join(e.command[1:])
    if txt:
        msg = str(txt)
    elif e.reply_to_message:
        msg = e.reply_to_message.text.markdown
    else:
        await e.reply_text("Give Message for Broadcast or reply to any msg")
        return

    Han = await e.reply_text("Broadcasting...")
    err = 0
    dn = 0
    data = users.get_all_users()
    for x in data:
       try:
          await RiZoeL.send_message(x.user_id, msg)
          await asyncio.sleep(0.5)
          dn += 1
       except Exception as a:
          print(a)
          err += 1
    try:
       await Han.edit_text(f"Broadcast Done ✓ \n\n Success chats: {dn} \n Failed chats: {err}")
    except:
       await Han.delete()
       await e.reply_text(f"Broadcast Done ✓ \n\n Success chats: {dn} \n Failed chats: {err}")


@RiZoeL.on_message(filters.user(DEVS) & filters.command(["fcast", "fmsg", "forward", "forwardmessage"]))
async def forward_(_, e: Message):
    Siu = "".join(e.text.split(maxsplit=1)[1:]).split(" ", 1)
    if len(Siu) == 2:
       from_chat = str(Siu[0])
       Msg_id = int(Siu[1])      
    else:
       await e.reply_text("Wrong Usage! \n\n Syntax: /forward (from chat id) (message id) \n\nNote: Must add bot in from message Channel!")
       return

    Han = await e.reply_text("forwarding...")
    err = 0
    dn = 0
    data = users.get_all_users()
    for x in data:
       try:
          await RiZoeL.forward_messages(x.user_id, from_chat, Msg_id)
          await asyncio.sleep(0.5)
          dn += 1
       except Exception as a:
          print(a)
          err += 1
    try:
       await Han.edit_text(f"Done ✓ \n\n Success chats: {dn} \n Failed chats: {err}")
    except:
       await Han.delete()
       await e.reply_text(f"Done ✓ \n\n Success chats: {dn} \n Failed chats: {err}")
