import Data.conf


async def admin_add_products_edit_db(id_product: int, quantity: int):
    """
    Увеличение количества товара в магазине
    :param id_product:
    :param quantity:
    :return:
    """
    async with Data.conf.pool.acquire() as cursor:
        await cursor.execute("""
                            UPDATE products SET quantity = quantity + $2
                            WHERE products.id = $1
                            """,
                             id_product, quantity)


async def admin_del_products_edit_db(id_product: int, quantity: int):
    """
    Уменьшение товара в мазашине
    :param id_product:
    :param quantity:
    :return:
    """
    async with Data.conf.pool.acquire() as cursor:
        await cursor.execute("""
                            UPDATE products SET quantity = quantity - $2
                            WHERE products.id = $1
                            """,
                             id_product, quantity)


async def admin_cost_products_edit_db(id_product: int, cost: float):
    """
    Изменение стоимости товара
    :param id_product:
    :param cost:
    :return:
    """
    async with Data.conf.pool.acquire() as cursor:
        await cursor.execute("""
                            UPDATE products SET cost = $2
                            WHERE products.id = $1 
                            """,
                             id_product, cost)


async def admin_description_products_edit_db(id_product: int, description: str):
    """
    Изменение описания продукта
    :param id_product:
    :param description:
    :return:
    """
    async with Data.conf.pool.acquire() as cursor:
        await cursor.execute("""
                            UPDATE products SET description = $2
                            WHERE products.id = $1 
                            """,
                             id_product, description)



async def admin_photo_products_edit_db(id_product: int, photo: str):
    """
    обновление фотографии
    :param id_product:
    :param photo:
    :return:
    """
    async with Data.conf.pool.acquire() as cursor:
        await cursor.execute("""
                            UPDATE products SET image = $2
                            WHERE products.id = $1
                            """,
                            id_product, photo)

    # print('отправлено', id_product, photo)






