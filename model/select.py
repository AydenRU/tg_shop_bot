from utils.exceptions_dlia_my import ExceptionsCheck

import Data.conf



@ExceptionsCheck.check_exception
async def get_id_product(name: str):
    """
    Получение id продукта
    :param name:
    :return:
    """
    async with Data.conf.pool.acquire() as cursor:
        answer = await cursor.fetchrow("""
                                        SELECT id FROM products
                                            WHERE products.nameproduct = $1
                                        """,
                                       name)
        return answer


@ExceptionsCheck.check_exception
async def get_quantity_product_db(id_product: int):
    """
    Получение количество товара
    :param id_product:
    :return:
    """
    async with Data.conf.pool.acquire() as cursor:
        answer = await cursor.fetchrow("""
                                        SELECT quantity FROM products
                                            WHERE products.id = $1
                                        """,
                                       id_product)
        # print(type(answer))
        return answer


@ExceptionsCheck.check_exception
async def get_total_cost(id_users):
    """
    Получение суммы корзины
    :param id_users:
    :return:
    """
    async with Data.conf.pool.acquire() as cursor:
        total = await cursor.fetchval("""
                                      SELECT SUM(baskets.quantity * products.cost) FROM baskets
                                        JOIN products ON products.id = baskets.id_product
                                        WHERE baskets.id_users = $1
                                      """,
                                      id_users)
        # print(type(total))
    return total


@ExceptionsCheck.check_exception
async def get_quantity_basket(id_product: int, id_user: int):
    """
    получение количество товара в корзине пользователя
    :param id_product:
    :param id_user:
    :return:
    """
    async with Data.conf.pool.acquire() as cursor:
        answer = await cursor.fetchrow("""
                                    SELECT baskets.quantity FROM baskets
                                        WHERE baskets.id_users = $1 and baskets.id_product = $2 ;
                                    """,
                                    id_user, id_product)
    return answer



@ExceptionsCheck.check_exception
async def get_basket_db(id_user: int):
    """
    Получаем корзину пользователя по id
    products.id, products.nameproduct, baskets.quantity, products.cost
    :id: уникальный номер пользователя
    """
    async with Data.conf.pool.acquire() as cursor:
        answer = await cursor.fetch("""
                                    SELECT products.id, products.nameproduct, baskets.quantity, products.cost FROM users
                                        JOIN baskets ON users.id = baskets.id_users
                                        JOIN products ON baskets.id_product = products.id
                                        WHERE users.id = $1;
                                    """,
                                    id_user)
        # print(type(answer[0]))
    return answer



@ExceptionsCheck.check_exception
async def get_list_products_db():
    """
    Возвращает все продукты, которые есть в наличии
    :return:
    """
    async with Data.conf.pool.acquire() as cursor:
        answer = await cursor.fetch("""
                                    SELECT id, nameproduct, cost FROM products
                                    WHERE is_active is true;
                                    """)
        # print(answer)
        return answer


@ExceptionsCheck.check_exception
async def get_info_about_product_db(id_product: int):
    """
    введя id товара получишь данные о нем
    :param id_product:
    :return:
    """
    async with Data.conf.pool.acquire() as cursor:
        answer = await cursor.fetchrow("""
                                        SELECT * FROM products
                                            WHERE products.id = $1
                                        """,
                                       id_product)
    return answer

# Запросы платежей

@ExceptionsCheck.check_exception
async def get_status_payment(id_users: int) :
    """
    Возвращает status_payments, id_payments*
    :param id_users:
    :return:
    """
    async with Data.conf.pool.acquire() as cursor:
        answer = await cursor.fetchrow("""
                                        SELECT status_payments, id_payments, url_pay FROM history
                                        WHERE history.id_users = $1 and history.status_payments = $2
                                        """,
                                       id_users, 'pending')
        print(answer)
    return answer


@ExceptionsCheck.check_exception
async def get_status_pending_payment(id_users: int) -> list[dict]:
    """Получение статуса оплаты заказа пользователя"""
    async with Data.conf.pool.acquire() as cursor:
        answer = await cursor.fetch("""
                                        SELECT status_payments, id_payments, url_pay FROM history
                                        WHERE history.id_users = $1 
                                        AND history.status_payments = $2
                                        """,
                                       id_users, 'pending')

    return answer

#Запросы о заказе

@ExceptionsCheck.check_exception
async def get_data_order_user(id_user):
    """Получение данных об заказе пользователя"""
    async with Data.conf.pool.acquire() as cursor:
        answer = await cursor.fetchrow("""
                            SELECT * FROM orders
                                WHERE id_users = $1 AND order_status != 'Доставлен'
                            """,
                            id_user)


    return answer


@ExceptionsCheck.check_exception
async def get_order_status(id_user) -> dict:
    """
    Получение статуса заказа пользователя
    :param id_user:
    :return: dict[str[order_status]]
    """
    async with Data.conf.pool.acquire() as cursor:
        answer = await cursor.fetchrow("""
                                    SELECT order_status FROM orders
                                        WHERE id_users = $1
                                        AND order_status != $2
                                    """,
                                    id_user, 'Доставлен')
    return answer


@ExceptionsCheck.check_exception
async def get_data_order_users():
    """
    Получение данных заказа при его полной доставке
    :return:
    """
    async with Data.conf.pool.acquire() as cursor:
        answer = await cursor.fetch("""
                            SELECT * FROM orders
                                WHERE order_status != $1
                            """,
                            'Доставлен')
    # print(answer)
    return answer

@ExceptionsCheck.check_exception
async def get_is_order(id_user) -> bool:
    """
    Проверка на наличие заказов
    :param id_user:
    :return:
    """
    async with Data.conf.pool.acquire() as cursor:
        answer = await cursor.fetchrow("""
                                        SELECT id FROM orders
                                            WHERE id_users = $1 AND order_status != $2
                                        """,
                                       id_user, 'Доставлен')
    return False if answer else True
