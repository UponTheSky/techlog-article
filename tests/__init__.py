from unittest import mock

from techlog_article.common.database import utils

# this is for mocking the decorators
# for details: https://www.freblogg.com/pytest-functions-mocking-1
mock.patch.object(utils, "transactional", lambda x: x).start()
