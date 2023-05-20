from unittest import mock

from techlog_article.common.database import utils

# this is for mocking the decorators
# for details: https://www.freblogg.com/pytest-functions-mocking-1
mock.patch.object(utils, "transactional", lambda x: x).start()

# this is for mocking Mangum
# since as it wraps the app object we lose the interface for the controller tests
mock.patch("mangum.Mangum", lambda x: x).start()
