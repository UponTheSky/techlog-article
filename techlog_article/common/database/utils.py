from typing import Callable, Awaitable, Any
import functools

from ..utils.logger import get_logger
from ._session import get_current_session, get_db_session_context


AsyncCallable = Callable[..., Awaitable]
logger = get_logger(filename=__file__)


def transactional(func: AsyncCallable) -> AsyncCallable:
    @functools.wraps(func)
    async def _wrapper(*args, **kwargs) -> Awaitable[Any]:
        try:
            db_session = get_current_session()

            if db_session.in_transaction():
                return await func(*args, **kwargs)

            async with db_session.begin():
                # automatically committed / rolled back thanks to the context manager
                return_value = await func(*args, **kwargs)

            return return_value
        except Exception as error:
            logger.info(f"request hash: {get_db_session_context()}")
            logger.exception(error)
            raise

    return _wrapper
