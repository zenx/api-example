from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from repositories.config import Base


class ArtistTable(Base):
    __tablename__ = "artist"

    id = Column(Integer, primary_key=True)
    name = Column(Text, index=True, unique=True)
    biography = Column(Text)
    albums = relationship('AlbumTable', back_populates='artist')

    def __repr__(self):
        return "repositories.ArtistTable: {}".format(self.name)
