from Exception import Exception_c

import Data.conf


# Пользователь

class Edit_users:
    @staticmethod
    @Exception_c.check_exception
    async def new_user(id):
        """Добавление нового пользователя,
         если он уже существует то выдаст исключение"""
        # print(model.conf.pool)
        async with Data.conf.pool.acquire() as cursor:
            await cursor.execute("""
                                INSERT INTO  users (id)
                                VALUES ($1)
                                    ON CONFLICT DO NOTHING
                                """,
                                 id)

@Exception_c.check_exception
async def products_in_baskets_db(id_user: int, id_product: int, quantity: int= 1):
    async with Data.conf.pool.acquire() as cursor:
        async with cursor.transaction():
            await cursor.execute("""UPDATE products
                                SET quantity = products.quantity - $2
                                WHERE id = $1
                                """,
                                 id_product, quantity)
            print('Товар вычтен из каталога продуктов')

            await cursor.execute("""
                                INSERT INTO baskets (id_users, id_product, quantity)
                                    VALUES ($1, $2, $3)
                                    ON CONFLICT (id_product, id_users) DO
                                    UPDATE SET quantity = baskets.quantity + $3
                                """,
                                 id_user, id_product, quantity)
            print(f'Товар {id_product} добавлен в корзину')

@Exception_c.check_exception
async def put_basket_in_products_db(id_user: int, id_product: int, quantity: int= 0):
    async with Data.conf.pool.acquire() as cursor:
        async with cursor.transaction():
            await cursor.execute("""
                                UPDATE baskets
                                SET quantity = quantity - $3
                                        WHERE baskets.id_users = $1 and baskets.id_product = $2
                                """,
                                 id_user, id_product, quantity)

            print('Товар вычтен из корзины продуктов')
            await cursor.execute("""
                                UPDATE products
                                SET quantity = quantity + $2
                                    WHERE id = $1
                                """,
                                 id_product, quantity)

            print(f'Товар {id_product} добавлен в корзину')

@Exception_c.check_exception
async def delete_basket_in_products_db(id_user: int, id_product: int, quantity: int):
    async with Data.conf.pool.acquire() as cursor:
        async with cursor.transaction():
            await cursor.execute("""
                                DELETE FROM baskets 
                                    WHERE baskets.id_users = $1 and baskets.id_product = $2
                                """,
                                 id_user, id_product)

            print('Товар вычтен из корзины продуктов')
            await cursor.execute("""
                                UPDATE products
                                SET quantity = quantity + $2
                                    WHERE id = $1
                                """,
                                 id_product, quantity)

            print(f'Товар {id_product} добавлен в корзину')




# Администратор

@Exception_c.check_exception
async def admin_add_products_db(data):
    async with Data.conf.pool.acquire() as cursor:
        await cursor.execute("""
                            INSERT INTO products (nameproduct, cost, quantity)
                            VALUES ($1, $2, $3)
                            """, data[0], data[1], int(data[2]))
    print('Данные добавлены')


@Exception_c.check_exception
async def admin_get_list_products_db():
    async with Data.conf.pool.acquire() as cursor:
        answer = await cursor.fetch("""
                                    SELECT id, nameproduct, quantity, cost FROM products
                                    """)
        return answer


@Exception_c.check_exception
async def admin_del_products_db(id_product: int):
    try:
        async with Data.conf.pool.acquire() as cursor:
            await cursor.execute("""
                                DELETE FROM products
                                WHERE products.id = $1
                                """, id_product)
        return True
    except Exception as error:
        print(error)
        return False
