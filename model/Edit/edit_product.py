from Exception import Exception_c

import Data.conf
from model.change import admin_add_products_db


async def admin_add_products_edit_db(id_product: int, quantity: int):
    async with Data.conf.pool.acquire() as cursor:
        await cursor.execute("""
                            UPDATE products SET quantity = quantity + $2
                            WHERE products.id = $1
                            """,
                             id_product, quantity)


async def admin_del_products_edit_db(id_product: int, quantity: int):
    async with Data.conf.pool.acquire() as cursor:
        await cursor.execute("""
                            UPDATE products SET quantity = quantity - $2
                            WHERE products.id = $1
                            """,
                             id_product, quantity)


async def admin_cost_products_edit_db(id_product: int, cost: float):
    async with Data.conf.pool.acquire() as cursor:
        await cursor.execute("""
                            UPDATE products SET cost = $2
                            WHERE products.id = $1 
                            """,
                             id_product, cost)

async def admin_description_products_edit_db(id_product: int, description: str):
    async with Data.conf.pool.acquire() as cursor:
        await cursor.execute("""
                            UPDATE products SET description = $2
                            WHERE products.id = $1 
                            """,
                             id_product, description)






