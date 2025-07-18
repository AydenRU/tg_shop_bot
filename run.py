import aiogram
import asyncio
import os

from dotenv import load_dotenv
from model.connection_db import connection_bd, test_connection_bd

from handlers.pages.main import router_main
from handlers.pages.product import router_product
from handlers.pages.basket import  router_basket

from handlers.tech_support.send_message_in_support import router_send_message_in_support

from handlers.admin.admin_handler import router_admin
from handlers.admin.del_product import router_del_product_admin
from handlers.admin.add_product import router_add_new_product_admin
from handlers.admin.edit_product import router_edit_product_admin

from handlers.admin.edit.description import router_description_product
from handlers.admin.edit.delete import router_del_product
from handlers.admin.edit.cost import router_cost_product
from handlers.admin.edit.add import router_add_product
from handlers.admin.edit.photo import router_photo_product

from handlers.admin.order_status.edit_order import edit_order_router
from handlers.admin.order_status.main_list_order import main_list_order_router

from pay.pay import router_pay
from pay.user_data import user_data_router

import Data.conf

load_dotenv()
bot = aiogram.Bot(token=os.getenv("TOKEN"))


disp = aiogram.Dispatcher()


async def main():
    """
    Запуск БД, соединение с роутерами и пуллинг тг
    :return:
    """
    await connection_bd()
    await test_connection_bd(Data.conf.pool)

    disp.include_router(router_main)
    disp.include_router(router_admin)
    disp.include_router(router_product)
    disp.include_router(router_basket)
    disp.include_router(router_send_message_in_support)
    disp.include_router(router_del_product_admin)
    disp.include_router(router_add_new_product_admin)
    disp.include_router(router_edit_product_admin)
    disp.include_router(router_add_product)
    disp.include_router(router_del_product)
    disp.include_router(router_cost_product)
    disp.include_router(router_description_product)
    disp.include_router(router_pay)
    disp.include_router(main_list_order_router)
    disp.include_router(edit_order_router)
    disp.include_router(user_data_router)
    disp.include_router(router_photo_product)

    try:
        await disp.start_polling(bot)
    except KeyboardInterrupt as error:
        print('Покааааа')
    # finally:
        # for i in [984778593]:
            # await bot.send_message(chat_id=i, text='Я ухожу спать :=(')

if __name__ == '__main__':
    asyncio.run(main())


