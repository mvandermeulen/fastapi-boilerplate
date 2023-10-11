from datetime import datetime
from enum import Enum

from fastapi import Query

from app.schemas.core import BaseSchema
from app.schemas.core import PagingMeta
from app.schemas.core import SortQueryIn


class FileBase(BaseSchema):
    link: str
    public_id: str
    filename: str
    file_type: str


class FileCreate(FileBase):
    pass


# Properties to receive via API on update
class FileUpdate(BaseSchema):
    pass


class FileResponse(FileBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FilesPagedResponse(BaseSchema):
    data: list[FileResponse] | None
    meta: PagingMeta | None


class FileSortFieldEnum(Enum):
    created_at = "created_at"


class FileSortQueryIn(SortQueryIn):
    sort_field: FileSortFieldEnum | None = Query(FileSortFieldEnum.created_at)
