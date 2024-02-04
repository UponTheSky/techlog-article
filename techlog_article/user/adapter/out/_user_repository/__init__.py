from techlog_article.common.config import config

if config.DB_TYPE == "postgres":
    from ._postgres import *  # noqa F403

else:  # config.DB_TYPE == "firestore"
    ...
    # TODO: implement the firestore version
