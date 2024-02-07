from models import Battle, Player, session
from loguru import logger
import pandas as pd
from algorithm import realize_tournament, instantiate_players


def main(players: list[str]= None, cmp = None):
    try:
        if session.query(Player).first() is not None:
            # choice = input('There is already a tournament in the database, do you want to delete it? [y/n] ')
            choice = 'y'
            if choice == 'y':
                session.query(Player).delete()
                session.query(Battle).delete()
                session.commit()
                if players is None:
                    players = list(pd.read_csv('players.csv', header=None, names=['name'])['name'])
                players_object_list = instantiate_players(players)
                ranked_players = 0
            else:
                players_object_list = session.query(Player).all()
                players_object_list = [player for player in players_object_list if player.rank is None]
                ranked_players = len(session.query(Player).filter(Player.rank != None).all())
        else:     
            logger.info('Received players list, debug mode')
            ranked_players = 0
            players_object_list = instantiate_players(players)

        for i in range(1 + ranked_players, len(players_object_list) + 1 + ranked_players):
            players_object_list_copy = players_object_list.copy()
            winner = realize_tournament(players_object_list_copy, cmp)
            winner.rank = i
            logger.info(f'Winner is {winner.name}, rank {winner.rank}')
            session.add(winner)
            session.commit()
            players_object_list.remove(winner)
            # input('Progress saved. Press enter to continue')

        logger.info('Tournament finished')
    except Exception as ex:
        logger.warning(f'Exception: {ex}')
        session.rollback()


if __name__ == '__main__':
        
    # from pandas import read_csv
    # players = read_csv('test/animes.csv')['name']
    main(
        # players
        )