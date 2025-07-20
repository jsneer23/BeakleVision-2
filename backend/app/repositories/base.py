from typing import Generic, TypeVar

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

ModelT = TypeVar('ModelT', bound=SQLModel)
CreateT = TypeVar('CreateT', bound=SQLModel)

class BaseRepository(Generic[ModelT, CreateT]):

    def __init__(self, session: AsyncSession, base_type: type[ModelT], create_type: type[CreateT]):
        self.session: AsyncSession = session
        self.model_type: type[ModelT] = base_type
        self.create_type: type[CreateT] = create_type

    async def create(self, model: type[CreateT]) -> ModelT:
        db_obj = self.model_type.model_validate(model)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def upsert(self, update_model: type[CreateT]) -> ModelT:

        model = self.model_type.model_validate(update_model)
        db_model = await self.session.merge(model)
        await self.session.commit()
        await self.session.refresh(db_model)
        return db_model

    async def delete(self, model: ModelT) -> None:
        await self.session.delete(model)
        await self.session.commit()

    async def get_by_key(self, key: str) -> ModelT | None:
        return await self.session.get(self.model_type, key=key)
