from .redis_crud import redis_conn
from .user_async import user
from app import models
from app import schemas
from app.crud.crud_async_base import CRUDAsyncBase
from app.crud.crud_sync_base import CRUDSyncBase

user_sync: CRUDSyncBase[
    models.User,
    schemas.UserCreate,
    schemas.UserUpdate,
    schemas.UserResponse,
    schemas.UsersPagedResponse,
] = CRUDSyncBase(
    model=models.User,
    response_schema_class=schemas.UserResponse,
    list_response_class=schemas.UsersPagedResponse,
)

notification_sync: CRUDSyncBase[
    models.Notification,
    schemas.NotificationCreate,
    schemas.NotificationUpdate,
    schemas.NotificationResponse,
    schemas.NotificationsPagedResponse,
] = CRUDSyncBase(
    model=models.Notification,
    response_schema_class=schemas.NotificationResponse,
    list_response_class=schemas.NotificationsPagedResponse,
)

file_async: CRUDAsyncBase[
    models.File,
    schemas.FileCreate,
    schemas.FileUpdate,
    schemas.FileResponse,
    schemas.FilesPagedResponse,
] = CRUDAsyncBase(
    model=models.File,
    response_schema_class=schemas.FileResponse,
    list_response_class=schemas.FilesPagedResponse,
)
