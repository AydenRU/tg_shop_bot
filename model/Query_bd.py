import asyncpg

from asyncpg import Pool

# from model.conf import pool
import model.conf


async def check_user():
    pass

async def new_user(id):
    """Добавление нового пользователя,
     если он уже существует то выдаст исключение"""
    print(model.conf.pool)
    try:
        if model.conf.pool is None:
            raise RuntimeError("🔴 Database pool not initialized")

        async with model.conf.pool.acquire() as cursor:
            await cursor.execute("""INSERT INTO  users (id)
                                VALUES ($1)
                                ON CONFLICT
                                DO NOTHING""",
                                id)
    except Exception as error:
        print(error)

async def get_basket_db(id):
    try:
        async with model.conf.pool.acquire() as cursor:
            answer = await cursor.fetch("""
                                        SELECT products.id, products.nameproduct, baskets.quantity, products.cost FROM users
                                        JOIN baskets ON users.id = baskets.id_users
                                        JOIN products ON baskets.id_product = products.id
                                        WHERE users.id = $1;
                                        """, id)
            print(type(answer[0]))
        return answer
    except Exception as error:
        print(error)