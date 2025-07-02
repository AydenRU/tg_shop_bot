import aiogram
import asyncio
import os

from dotenv import load_dotenv
from model.connection_db import connection_bd, test_connection_bd

from request.pages.main import router_main
from request.pages.product import router_product
from request.pages.basket import  router_basket

from request.admin.admin_handler import router_admin
from request.admin.del_product import router_del_product_admin
from request.admin.add_product import router_add_new_product_admin
from request.admin.edit_product import router_edit_product_admin

from request.admin.edit.description import router_description_product
from request.admin.edit.delete import router_del_product
from request.admin.edit.cost import router_cost_product
from request.admin.edit.add import router_add_product

from pay.pay import router_pay

import Data.conf

load_dotenv()
bot = aiogram.Bot(token=os.getenv("TOKEN"))


disp = aiogram.Dispatcher()


async def main():
    await connection_bd()
    await test_connection_bd(Data.conf.pool)

    disp.include_router(router_main)
    disp.include_router(router_admin)
    disp.include_router(router_product)
    disp.include_router(router_basket)
    disp.include_router(router_del_product_admin)
    disp.include_router(router_add_new_product_admin)
    disp.include_router(router_edit_product_admin)
    disp.include_router(router_add_product)
    disp.include_router(router_del_product)
    disp.include_router(router_cost_product)
    disp.include_router(router_description_product)
    disp.include_router(router_pay)

    await disp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())


