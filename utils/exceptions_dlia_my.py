from functools import wraps

from aiogram.types import CallbackQuery





class ExceptionsCheck:

    @staticmethod
    def check_exception(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args)
            except Exception as error:
                print(f"{func} {error}")
                result = []
            return result if result else []

        return wrapper

    @staticmethod
    def check_payment_status_pending(func):
        from pay.pay import StatusPayment
        @wraps(func)
        async def wrapper(callback: CallbackQuery, *args, **kwargs):
            id_user = callback.from_user.id
            check = await StatusPayment.check_status(id_user)

            if check:
                await callback.message.answer(
                    text="У вас уже есть незавершённый платёж. Завершите его или отмените перед изменением корзины."
                )
                return None
            return await func(callback, *args, **kwargs)

        return wrapper
