from random import randint

def main () :
    name = input("Введите имя игрока:")
    hero = Hero(name)
    game_round = GameRound(hero)
    game_round.play()
    print ("Вы набрали", hero.get_scores(), "очков")


class BattleUnit:
    """
    Отвечает за здоровье и атаку.
    """
    def __init__(self, health, attack_force):
        self._health = health
        self._attack_force = attack_force

    def get_health(self):
        return self._health

    def cause_damage(self, other):
        """Причинить урон другой боевой единице."""
        pass