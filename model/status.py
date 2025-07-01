from Exception import Exception_c

import Data.conf


class CheckStatus:
    @staticmethod
    @Exception_c.check_exception
    async def check_user(id) -> bool:
        async with Data.conf.pool.acquire() as cursor:
            answer = await cursor.fetch("""
                                        SELECT status_accsess FROM users
                                        WHERE users.id = $1
                                        """,
                                        id)
        return bool(answer[0]['status_accsess'])