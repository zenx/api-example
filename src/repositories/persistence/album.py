from sqlalchemy import Column, Integer, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from repositories.config import Base


class AlbumTable(Base):
    __tablename__ = "album"
    __table_args__ = (UniqueConstraint('artist_id', 'title', name='_artist_album_uc'),)

    id = Column(Integer, primary_key=True)
    title = Column(Text, index=True)
    artist_id = Column(Integer, ForeignKey('artist.id'))
    artist = relationship('ArtistTable', back_populates='albums')
    songs = relationship('SongTable', back_populates='album')
    likes = Column(Integer, index=True)

    def __repr__(self):
        return "repositories.AlbumTable: {}".format(self.title)
