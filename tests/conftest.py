import asyncio

import pytest


@pytest.fixture(scope="session")
def event_loop():
    """
    Since we'll use a db_session as session-scoped object, the event loop must
    also be of the same scope

    At the beginning, this fixture was in adapter/out, which caused early-cleanup
    of the eventloop as soon as all the tests in adapter/out have finished.

    Therefore, this eventloop fixture must be at the top level of the test directories.

    for details see:
    https://pytest-asyncio.readthedocs.io/en/latest/reference/fixtures.html#event-loop
    """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()

    yield loop

    loop.close()
