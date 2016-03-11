from sqlalchemy import Column, Integer, ForeignKey, Table, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from repositories.config import Base

association_table = Table('association', Base.metadata,
    Column('song_id', Integer, ForeignKey('song.id')),
    Column('artist_id', Integer, ForeignKey('artist.id'))
)


class SongTable(Base):
    __tablename__ = "song"
    __table_args__ = (UniqueConstraint('album_id', 'title', name='_album_song_uc'),)

    id = Column(Integer, primary_key=True)
    title = Column(Text, index=True)
    # duration in seconds
    duration = Column(Integer, nullable=True)
    album_id = Column(Integer, ForeignKey('album.id'))
    album = relationship('AlbumTable', back_populates='songs')
    featuring_artists = relationship('ArtistTable',
                            secondary=association_table,
                            backref='featuring_songs')

    def __repr__(self):
        return "repositories.SongTable: {}".format(self.title)
