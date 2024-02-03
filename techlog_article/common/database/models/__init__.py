from ...config import config

if config.DB_TYPE == "postgres":
    from .postgres import *  # noqa: F403

elif config.DB_TYPE == "firestore":
    from .firestore import *  # noqa: F403
