import asyncpg
import asyncio
import time

import model.conf


async def connection_bd():
    model.conf.pool = await asyncpg.create_pool(host='localhost', database='AydenShopBot', password='postgres', user='postgres',
                                     min_size=1, max_size=3)
    print('Подключение с БД произведено')


async def test_connection_bd(pool):

    async with pool.acquire() as cursor:
            print(await cursor.fetch("""SELECT version()"""))