from sqlalchemy import Column
from sqlalchemy import String

from app.models.base import Base
from app.models.base import ModelBaseMixinWithoutDeletedAt


class File(ModelBaseMixinWithoutDeletedAt, Base):
    link = Column(String, nullable=False)
    public_id = Column(String, nullable=False)
    filename = Column(String, nullable=True)
    file_type = Column(String, nullable=False)
