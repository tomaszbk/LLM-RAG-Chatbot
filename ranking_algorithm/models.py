from sqlalchemy import create_engine, ForeignKey, CheckConstraint, ForeignKeyConstraint
from sqlalchemy.orm import relationship,mapped_column, Mapped
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

class Battle(Base):
    __tablename__ = 'battles'
    __table_args__ = (
        CheckConstraint("player1_id > player2_id", name="player_ids_order_check"),
        ForeignKeyConstraint(
            ["player1_id"],
            ["players.id"],
            name="p1_id_fkey",
        ),
        ForeignKeyConstraint(
            ["player2_id"], ["players.id"], name="p2_id_fkey"
        )
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    player1_id: Mapped[int] = mapped_column(ForeignKey('players.id'))
    player2_id: Mapped[int] = mapped_column(ForeignKey('players.id'))
    winner_id: Mapped[int] = mapped_column(ForeignKey('players.id'))
    loser_id: Mapped[int] = mapped_column(ForeignKey('players.id'))
    player1: Mapped["Player"] = relationship('Player', foreign_keys=[player1_id], uselist=False)
    player2: Mapped["Player"] = relationship('Player', foreign_keys=[player2_id], uselist=False)
    winner: Mapped["Player"] = relationship('Player', back_populates='won_battles', foreign_keys=[winner_id])
    loser: Mapped["Player"] = relationship('Player', back_populates='lost_battles', foreign_keys=[loser_id])
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2


class Player(Base):
    __tablename__ = 'players'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    rank: Mapped[int] = mapped_column(unique=True, nullable=True)
    
    battles: Mapped[list["Battle"]] = relationship('Battle',back_populates='player1', foreign_keys=[Battle.player1_id])
    battles2: Mapped[list["Battle"]] = relationship('Battle',back_populates='player2', foreign_keys=[Battle.player2_id])
    won_battles: Mapped[list["Battle"]] = relationship('Battle', back_populates='winner', foreign_keys=[Battle.winner_id])
    lost_battles: Mapped[list["Battle"]] = relationship('Battle', back_populates='loser', foreign_keys=[Battle.loser_id])
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        if isinstance(other, Player):
            return self.name == other.name
        return False
    
    def __hash__(self):
        return hash(self.id)


DATABASE_URL = "sqlite:///ranking.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()