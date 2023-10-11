from typing import Annotated
from typing import Any
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import HTTPException
from fastapi import status
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app import schemas
from app.core.cloud_storage.cloud_storage import CloudinaryStorage
from app.core.config import settings
from app.db.session import get_async_db

router = APIRouter()
storage = CloudinaryStorage(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
)


@router.get("/", operation_id="get_all_files")
async def get_all_files(
    q: str | None = None,
    paging_query_in: schemas.PagingQueryIn = Depends(),
    sort_query_in: schemas.FileSortQueryIn = Depends(),
    db: AsyncSession = Depends(get_async_db),
) -> schemas.FilesPagedResponse:
    files = await crud.file_async.get_paged_list(db=db, paging_query_in=paging_query_in)
    return files


@router.get(
    "/{id}",
    operation_id="get_file_by_id",
)
async def get_file_by_id(
    id: str,
    db: AsyncSession = Depends(get_async_db),
) -> schemas.FileResponse:
    file = await crud.file_async.get_db_obj_by_id(db, id=id)
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="file not found"
        )
    return file


@router.post(
    "/",
    description="",
    operation_id="upload_files",
    response_model=List[schemas.FileResponse],
)
async def upload_file(
    *,
    files: Annotated[list[UploadFile], File(...)],
    db: AsyncSession = Depends(get_async_db),
) -> Any:
    """
    Upload new image.
    """
    create_schemas = []
    for file in files:
        file_content = await file.read()

        result = storage.upload_file(
            file_content=file_content,
            filename=file.filename,
        )

        create_schemas.append(
            schemas.FileCreate(
                link=result.get("url"),
                public_id=result.get("public_id"),
                filename=file.filename,
                file_type=file.content_type,
            )
        )

    created_files = await crud.file_async.create_bulk(
        db=db, create_schemas=create_schemas
    )
    return created_files


@router.delete(
    "/{id}", status_code=status.HTTP_204_NO_CONTENT, operation_id="delete_file"
)
async def delete_file(
    id: str,
    db: AsyncSession = Depends(get_async_db),
) -> None:
    file = await crud.file_async.get_db_obj_by_id(db, id=id)
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="file not found"
        )
    storage.delete_file(file.public_id)
    await crud.file_async.real_delete(db, db_obj=file)
