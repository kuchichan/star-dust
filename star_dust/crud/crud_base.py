from typing import Any, Generic, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic.main import BaseModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select

from star_dust.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    async def get(
        self, session_db: AsyncSession, id_: Any, *, options: Any = None
    ) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.id == id_)
        stmt = stmt if not options else stmt.options(options)

        result = await session_db.execute(stmt)
        return result.scalars().first()

    async def create(
        self, session_db: AsyncSession, *, obj_in: CreateSchemaType
    ) -> ModelType:
        object_in_data = jsonable_encoder(obj_in)
        db_object = self.model(**object_in_data)  # type: ignore

        session_db.add(db_object)
        await session_db.commit()
        await session_db.refresh(db_object)

        return db_object
