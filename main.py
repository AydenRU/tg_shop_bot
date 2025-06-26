import aiogram
import asyncio


from model.connection_db import connection_bd, test_connection_bd
from requests.handler import router_main
import model.conf

# 7954528574:AAFdMPSO0pk2gQUEJdyhyC6W_a71QewDCfo


bot = aiogram.Bot(token='7954528574:AAFdMPSO0pk2gQUEJdyhyC6W_a71QewDCfo')

disp = aiogram.Dispatcher()


async def main():
    await connection_bd()
    await test_connection_bd(model.conf.pool)
    disp.include_router(router_main)

    await disp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())


