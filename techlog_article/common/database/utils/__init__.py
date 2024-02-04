from ...config import config

if config.DB_TYPE == "postgres":
    from ._postgres import transactional

else:  # config.DB_TYPE == "firestore"
    from ._firestore import transactional

__all__ = ["transactional"]
