from Exception import Exception_c

import model.conf



@Exception_c.check_exception
async def get_id_product(name: str):

    async with model.conf.pool.acquire() as cursor:
        answer = await cursor.fetchrow("""
                                        SELECT id FROM products
                                            WHERE products.nameproduct = $1
                                        """,
                                       name)
        return answer

@Exception_c.check_exception
async def get_quantity_basket(id_product: int, id_user: int):
    """

    :param id_product:
    :param id_user:
    :return:
    """
    async with model.conf.pool.acquire() as cursor:
        answer = await cursor.fetchrow("""
                                    SELECT baskets.quantity FROM baskets
                                        WHERE baskets.id_users = $1 and baskets.id_product = $2 ;
                                    """,
                                    id_user, id_product)
    return answer



@Exception_c.check_exception
async def get_basket_db(id_user: int):
    """
    Получаем корзину пользователя по id
    :id: уникальный номер пользователя
    """
    async with model.conf.pool.acquire() as cursor:
        answer = await cursor.fetch("""
                                    SELECT products.id, products.nameproduct, baskets.quantity, products.cost FROM users
                                        JOIN baskets ON users.id = baskets.id_users
                                        JOIN products ON baskets.id_product = products.id
                                        WHERE users.id = $1;
                                    """,
                                    id_user)
        # print(type(answer[0]))
    return answer



@Exception_c.check_exception
async def get_list_products_db():
    """
    Возвращает все продукты, которые есть в наличии
    :return:
    """
    async with model.conf.pool.acquire() as cursor:
        answer = await cursor.fetch("""
                                    SELECT id, nameproduct, cost FROM products
                                    WHERE is_active is true;
                                    """)
        # print(answer)
        return answer


@Exception_c.check_exception
async def get_info_about_product_db(id_product):
    """

    :param id:
    :return:
    """
    async with model.conf.pool.acquire() as cursor:
        answer = await cursor.fetchrow("""
                                        SELECT * FROM products
                                            WHERE products.id = $1
                                        """,
                                       id_product)
    return answer



