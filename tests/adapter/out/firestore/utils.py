from typing import Any, Optional, Mapping
from uuid import UUID

from pymongo.database import Database
from pymongo.client_session import ClientSession

from techlog_article.common.database import models

"""
General cases
"""


def db_commit(*, db_session: ClientSession) -> None:
    db_session.commit_transaction()


def store_single_entity(
    *,
    db_instance: Database,
    db_session: ClientSession,
    collection_name: str,
    document: Mapping,
) -> None:
    db_instance.get_collection(name=collection_name).insert_one(document)
    db_commit(db_session=db_session)


def read_single_entity_by_id(
    *, db_instance: Database, collection_name: str, id: UUID
) -> dict:
    return db_instance.get_collection(name=collection_name).find_one({"id": id})


def read_single_entity_by_field(
    *, db_instance: Database, collection_name: str, field_name: str, field_value: Any
) -> dict:
    return db_instance.get_collection(name=collection_name).find_one(
        {field_name: field_value}
    )


"""
Table-specific cases(due to relation, difficult to make as generic)
"""


def read_user_with_auth_by_username(
    *, db_instance: Database, username: str
) -> models.User:
    user = read_single_entity_by_field(
        db_instance=db_instance,
        collection_name="user",
        field_name="username",
        field_value=username,
    )
    assert user is not None

    return models.User(user)


async def read_article_with_user(
    *, db_instance: Database, db_session: ClientSession, article_id: UUID
) -> models.Article:
    article = read_single_entity_by_field(
        db_instance=db_instance,
        collection_name="article",
        field_name="id",
        field_value=article_id,
    )
    assert article is not None

    article = models.Article(article)
    user = read_single_entity_by_field(
        db_instance=db_instance,
        collection_name="user",
        field_name="id",
        field_value=article.author_id,
    )
    assert user is not None
    article.author = models.User(user)

    return article


def store_user_with_auth(
    *,
    db_instance: Database,
    db_session: ClientSession,
    user_id: str,
    username: str,
    email: str,
    hashed_password: str,
    access_token: str,
) -> None:
    user = models.User()

    store_single_entity(
        db_instance=db_instance,
        db_session=db_session,
        collection_name="user",
        document=user.to_dict(),
    )
    db_commit(db_session=db_session)


def store_user_with_article(
    *,
    db_instance: Database,
    db_session: ClientSession,
    user_id: UUID,
    username: str,
    article_id: UUID,
    article_title: str,
    content: Optional[str] = None,
) -> None:
    user = models.User(
        id=user_id,
        username=username,
        email="",
        hashed_password="",
        articles=[article_id],
    )

    article = models.Article(
        id=article_id, author_id=user_id, title=article_title, content=content
    )

    db_instance.get_collection("article").insert_one(article.to_dict())
    db_instance.get_collection("user").insert_one(user.to_dict())

    db_commit(db_session=db_session)
