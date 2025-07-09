from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class Resume(Base):
    __tablename__ = "resumes2"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(Text)
    raw_text = Column(Text)
    embedding = Column(Text)  # We will store as text for now
