from typing import final

from .port.in_ import CreateArticleInDTO, CreateArticleInPort
from .port.out import CreateArticleOutDTO, CreateArticleOutPort


@final
class CreateArticleService(CreateArticleInPort):
    def __init__(self, create_article_out_port: CreateArticleOutPort):  # TODO: DI
        self._create_article_out_port = create_article_out_port

    async def create_article(self, *, dto: CreateArticleInDTO) -> None:
        await self._create_article_out_port.create_article(
            dto=CreateArticleOutDTO(**dto.dict())
        )

        return None


@final
class ReadArticeService:
    ...


@final
class UpdateArticeService:
    ...


@final
class DeleteArticleService:
    ...
