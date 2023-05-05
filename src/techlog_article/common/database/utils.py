from typing import Callable, Awaitable, Any
import functools

from ._session import get_current_session

AsyncCallable = Callable[..., Awaitable]


def transactional(func: AsyncCallable) -> AsyncCallable:
    @functools.wraps(func)
    async def _wrapper(*args, **kwargs) -> Awaitable[Any]:
        db_session = get_current_session()

        if db_session.in_transaction():
            return await func(*args, **kwargs)

        async with db_session.begin():
            return_value = await func(*args, **kwargs)

        return return_value

    return _wrapper
