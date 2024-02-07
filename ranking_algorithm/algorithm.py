from models import Battle, Player, session
from loguru import logger
import random

counter = [0]

def realize_tournament_round(players: list[Player], cmp) -> list[Player]:
    """Realize a round of a tournament. ex: semifinals, quarterfinals, etc."""
    # logger.info(f'Starting round with {len(players)} players')
    battle_pairs: list[Battle] = create_battle_pairs(players)
    winners: list[Player] = []
    for battle in battle_pairs:
        battle_result_cache = battle_exists(battle)
        if battle_result_cache:
            # logger.debug(f'Battle {battle_result_cache.id} already exists')
            
            winners.append(battle_result_cache.winner)
            continue
        if battle.player1 == battle.player2:
            battle.winner = battle.player1
            winners.append(battle.winner)
            continue

        # print(f'--which one is better? {battle.player1.name}[1] or {battle.player2.name}[2]--')

        cmp(2,1)
        battle.winner = battle.player1
        battle.loser = battle.player2
       
        winners.append(battle.winner)
        session.add(battle)
        session.commit()
        win_against_loser_victories(winner=battle.winner, loser=battle.loser)

    return winners


def create_battle_pairs(players: list[Player]) -> list[Battle]:
    """Create a list of battles from a list of players"""
    if len(players) % 2 != 0:
        players.append(players[0])
    battle_pairs_list = []
    for i in range(0, len(players), 2):
        if players[i].id > players[i+1].id:
            battle_pairs_list.append(Battle(players[i], players[i+1]))
        else:
            battle_pairs_list.append(Battle(players[i+1], players[i]))
    
    return battle_pairs_list


def battle_exists(battle: Battle) -> Battle:
    """Check if a battle already exists in the database"""
    return session.query(Battle).filter(Battle.player1 == battle.player1, Battle.player2 == battle.player2).first()


def realize_tournament(players: list[Player], cmp) -> list[Player]:
    """Realize a tournament from a list of players"""
    random.shuffle(players)
    while len(players) > 1:
        players = realize_tournament_round(players, cmp)
        players = list(set(players)) # remove duplicates
    winner = players[0]
    return winner


def instantiate_players(players: list[str]) -> list[Player]:
    """Create a list of players from a list of names"""
    players_list = []
    for player in players:
        players_list.append(Player(player))
    session.add_all(players_list)
    session.commit()
    return players_list


def win_against_loser_victories(winner, loser):
    """Add a victory to the winner to every player the loser won to"""
    loser_victory_players = session.query(Battle).filter(Battle.winner_id == loser.id).all()
    for loser_victory_player in loser_victory_players:
        if not battle_exists(Battle(winner, loser_victory_player.loser)):
            new_battle = Battle(winner, loser_victory_player.loser) if winner.id > loser_victory_player.loser.id else Battle(loser_victory_player.loser, winner)
            new_battle.winner = winner
            new_battle.loser = loser_victory_player.loser
            session.add(new_battle)
            session.commit()