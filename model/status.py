from utils.exceptions_dlia_my import ExceptionsCheck

import Data.conf


class CheckStatus:
    """
    Получение прав пользователя в приложении
    """
    @staticmethod
    @ExceptionsCheck.check_exception
    async def check_user(id) -> bool:
        async with Data.conf.pool.acquire() as cursor:
            answer = await cursor.fetch("""
                                        SELECT status_accsess FROM users
                                        WHERE users.id = $1
                                        """,
                                        id)
        return bool(answer[0]['status_accsess'])