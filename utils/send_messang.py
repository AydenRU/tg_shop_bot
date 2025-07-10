from run import bot

async def message_user(id_users: int, text: str):
    await bot.send_message(text=text, chat_id=id_users)