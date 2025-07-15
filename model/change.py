from utils.exceptions_dlia_my import ExceptionsCheck

import Data.conf


# Пользователь

class Edit_users:
    @staticmethod
    @ExceptionsCheck.check_exception
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

@ExceptionsCheck.check_exception
async def products_in_baskets_db(id_user: int, id_product: int, quantity: int= 1):
    """
    Перенос товара из каталога товаров в корзину пользователя
    :param id_user:
    :param id_product:
    :param quantity:
    :return:
    """
    async with Data.conf.pool.acquire() as cursor:
        async with cursor.transaction():
            await cursor.execute("""UPDATE products
                                SET quantity = products.quantity - $2
                                WHERE id = $1
                                """,
                                 id_product, quantity)

            await cursor.execute("""
                                INSERT INTO baskets (id_users, id_product, quantity)
                                    VALUES ($1, $2, $3)
                                    ON CONFLICT (id_product, id_users) DO
                                    UPDATE SET quantity = baskets.quantity + $3
                                """,
                                 id_user, id_product, quantity)


@ExceptionsCheck.check_exception
async def put_basket_in_products_db(id_user: int, id_product: int, quantity: int= 0):
    """
    Перенос товара их корзины в каталог товаров
    :param id_user:
    :param id_product:
    :param quantity:
    :return:
    """
    async with Data.conf.pool.acquire() as cursor:
        async with cursor.transaction():
            await cursor.execute("""
                                UPDATE baskets
                                SET quantity = quantity - $3
                                        WHERE baskets.id_users = $1 and baskets.id_product = $2
                                """,
                                 id_user, id_product, quantity)

            await cursor.execute("""
                                UPDATE products
                                SET quantity = quantity + $2
                                    WHERE id = $1
                                """,
                                 id_product, quantity)



@ExceptionsCheck.check_exception
async def delete_basket_in_products_db(id_user: int, id_product: int, quantity: int):
    """
    Удаление товара из каталога товаров и корзин пользователей
    :param id_user:
    :param id_product:
    :param quantity:
    :return:
    """
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

@ExceptionsCheck.check_exception
async def admin_add_products_db(data):
    """
    Добавление товара в магазин
    :param data:
    :return:
    """
    async with Data.conf.pool.acquire() as cursor:
        await cursor.execute("""
                            INSERT INTO products (nameproduct, cost, quantity)
                            VALUES ($1, $2, $3)
                            """, data[0], data[1], int(data[2]))
    # print('Данные добавлены')


@ExceptionsCheck.check_exception
async def admin_get_list_products_db():
    """
    Получение списка товаров
    :return:
    """
    async with Data.conf.pool.acquire() as cursor:
        answer = await cursor.fetch("""
                                    SELECT id, nameproduct, quantity, cost FROM products
                                    """)
        return answer



async def admin_del_products_db(id_product: int):
    """
    Удаление товара из каталога
    :param id_product:
    :return:
    """
    try:
        async with Data.conf.pool.acquire() as cursor:
            await cursor.execute("""
                                DELETE FROM products
                                WHERE products.id = $1
                                """, id_product)
        return True
    except Exception as error:
        # print(error)
        return False


# Запросы платежей

@ExceptionsCheck.check_exception
async def insert_info_payment(id_users: int, id_payment: str, status: str, url: str):
    """
    Создание оплаты товара
    :param id_users:
    :param id_payment:
    :param status:
    :param url:
    :return:
    """
    async with Data.conf.pool.acquire() as cursor:
        await cursor.execute("""
                             INSERT INTO history (id_users, id_payments, status_payments, url_pay)
                                VALUES ($1,$2,$3,$4)
                             """,
                             id_users, id_payment, status, url)



@ExceptionsCheck.check_exception
async def update_status(id_user, id_payments, status):
    """
    Обновление статуса платежа
    :param id_user:
    :param id_payments:
    :param status:
    :return:
    """
    async with Data.conf.pool.acquire() as cursor:
        await cursor.execute("""
                            UPDATE history SET status_payments = $3
                                WHERE history.id_users = $1
                                AND history.id_payments = $2
                            """,
                             id_user, id_payments, status)


@ExceptionsCheck.check_exception
async def create_order(id_user, data_basket, data_users):
    """
    Создание заказа для сборки и отправки
    :param id_user:
    :param data_basket:
    :param data_users:
    :return:
    """
    async  with Data.conf.pool.acquire() as cursor:
        await  cursor.execute("""
                            INSERT INTO orders (id_users, order_data, order_status, name, contact, address)
                                VALUES ($1, $2, $3, $4, $5, $6 )
                            """,
                              id_user, data_basket, 'Оплачивается',
                              f"{data_users['last_name']} {data_users['first_name']}",
                              data_users['contact_data'], data_users['address'])

@ExceptionsCheck.check_exception
async def update_order(id_user: int, status: str ):
    """
    Существуют такие запросы ('Собирается', 'В пути', 'Доставлен')

    Если повысить статус до 'Доставлен', опустить его не получится
    :param id_user:
    :param status:
    :return:
    """
    async with Data.conf.pool.acquire() as cursor:
        await cursor.execute("""
                            UPDATE orders SET order_status = $2
                                WHERE id_users = $1 AND order_status != 'Доставлен'
                            """,
                             id_user, status)

@ExceptionsCheck.check_exception
async def delete_basket_user(id_users: int):
    """
    Удаление товара их корзины пользователя
    :param id_users:
    :return:
    """
    async with Data.conf.pool.acquire() as cursor:
        await cursor.execute("""
                            DELETE FROM baskets
                                WHERE id_users = $1
                            """,
                            id_users)
