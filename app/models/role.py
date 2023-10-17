from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.base import ModelBaseMixinWithoutDeletedAt


class Role(Base, ModelBaseMixinWithoutDeletedAt):
    description = Column(Text)
    label = Column(String(255))
    users = relationship("User", back_populates="role")
