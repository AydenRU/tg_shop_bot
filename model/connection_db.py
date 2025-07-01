import asyncpg
import os

import Data.conf

async def connection_bd():
    Data.conf.pool = await asyncpg.create_pool(host=os.getenv("HOST"), database=os.getenv("DATABASE"),
                                               password=os.getenv("PASSWORD"), user=os.getenv("USER"),
                                               min_size=1, max_size=3)
    print('Подключение с БД произведено')


async def test_connection_bd(pool):

    async with pool.acquire() as cursor:
            print(await cursor.fetch("""SELECT version()"""))