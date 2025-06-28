import asyncpg

from functools import wraps

from asyncpg import Pool

# from model.conf import pool
import model.conf


# Пользователь

def check_exception(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args)
        except Exception as error:
            print(error)
            result = []

        return result if result else []


    return wrapper


@check_exception
async def check_user(id) -> bool:

    async with model.conf.pool.acquire() as cursor:
        answer = await cursor.fetch("""
                                    SELECT status_accsess FROM users
                                    WHERE users.id = $1
                                    """, id)

        return bool(answer[0]['status_accsess'])



@check_exception
async def new_user(id):
    """Добавление нового пользователя,
     если он уже существует то выдаст исключение"""
    # print(model.conf.pool)
    async with model.conf.pool.acquire() as cursor:
        await cursor.execute("""
                            INSERT INTO  users (id)
                            VALUES ($1)
                                ON CONFLICT DO NOTHING""",
                             id)


@check_exception
async def get_basket_db(id):

    async with model.conf.pool.acquire() as cursor:
        answer = await cursor.fetch("""
                                    SELECT products.id, products.nameproduct, baskets.quantity, products.cost FROM users
                                        JOIN baskets ON users.id = baskets.id_users
                                        JOIN products ON baskets.id_product = products.id
                                        WHERE users.id = $1;
                                    """, id)
        # print(type(answer[0]))
    return answer


@check_exception
async def get_list_products_db():
    async with model.conf.pool.acquire() as cursor:
        answer = await cursor.fetch("""
                                    SELECT id, nameproduct, cost FROM products
                                    """)
        # print(answer)
        return answer


@check_exception
async def get_full_info_about_product_db(id):

    async with model.conf.pool.acquire() as cursor:
        answer = await cursor.fetchrow("""
                                        SELECT * FROM products
                                            WHERE products.id = $1
                                        """, int(id))
    return answer


@check_exception
async def get_full_info_about_product_db(id):
    async with model.conf.pool.acquire() as cursor:
        answer = await cursor.fetchrow("""
                                        SELECT * FROM products
                                            WHERE products.id = $1
                                        """, int(id))
    return answer


@check_exception
async def get_id_product(name: str):

    async with model.conf.pool.acquire() as cursor:
        answer = await cursor.fetchrow("""
                                        SELECT id FROM product
                                            WHERE product.name = $1""",
                                       name)
        return answer


@check_exception
async def products_in_baskets_db(id_user: int, id_product: int):

    async with model.conf.pool.acquire() as cursor:
        async with cursor.transaction():
            await cursor.execute("""UPDATE products
                                SET quantity = products.quantity - 1
                                WHERE id = $1
                                """, id_product)
            print('Товар вычтен из каталога продуктов')

            await cursor.execute("""
                                INSERT INTO baskets (id_users, id_product, quantity)
                                    VALUES ($1, $2, 1)
                                    ON CONFLICT (id_product, id_users) DO
                                    UPDATE SET quantity = baskets.quantity + 1                       
                                """,
                                 id_user, id_product)
            print(f'Товар {id_product} добавлен в корзину')


# Администратор

@check_exception
async def admin_add_products_db(data):
    async with model.conf.pool.acquire() as cursor:
        await cursor.execute("""
                            INSERT INTO products (nameproduct, cost, quantity)
                            VALUES ($1, $2, $3)
                            """, data[0], data[1], int(data[2]))
    print('Данные добавлены')


@check_exception
async def admin_get_list_products_db():
    async with model.conf.pool.acquire() as cursor:
        answer = await cursor.fetch("""
                                    SELECT id, nameproduct, quantity, cost FROM products
                                    """)
        return answer



async def admin_del_products_db(id_product: int):
    try:
        async with model.conf.pool.acquire() as cursor:
            await cursor.execute("""
                                DELETE FROM products
                                WHERE products.id = $1
                                """, id_product)
        return True
    except Exception as error:
        print(error)
        return False
