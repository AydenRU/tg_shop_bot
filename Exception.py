from functools import wraps

class Exception_c:
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