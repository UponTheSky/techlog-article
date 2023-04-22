from typing import Callable, Awaitable, Any
import functools

from ._session import AsyncScopedSession

AsyncCallable = Callable[..., Awaitable]


def transactional(func: AsyncCallable) -> AsyncCallable:
    @functools.wraps(func)
    async def _wrapper(*args, **kwargs) -> Awaitable[Any]:
        db_session = AsyncScopedSession()

        if db_session.in_transaction:
            return await func(*args, **kwargs)

        async with db_session.begin():
            return_value = await func(*args, **kwargs)

        return return_value

    return _wrapper
