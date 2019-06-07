import tcod
from gameMessages import Message

class Fighter:
    """ Provides basic fighting logic like health, attacks and defense.

    A class that can be used when creating entity instances, to allow them to partake in combat
    This class can be optionally handed to entities. It allows them to do combat, and to be attacked themselves.

    Parameters
    ----------
    max_hp : int
        The maximum hitpoints of the entity. Entities start out at this number of hitpoints.
    hp : int
        The current number of hitpoints this entity has.
    defense : int
        The number which is detracted from attacks on this entity when calculating damage.
    power : int
        The number of hitpoints this entity damages others for when it attacks.
    """
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power

    def take_damage(self,amount):
        """Deals damage to self.

        Used when an entity is being damaged, for example through attacks by other entities.

        Parameters
        ----------
        amount : int
            The number of hitpoints that will be subtracted.
        """
        results = []
        self.hp -= amount
        if self.hp <= 0:
            results.append({'dead':self.owner})
        return results

    def heal(self, amount):
        """A function that restores hitpoints to the entity
        Used when an entity is healed, for example through the use of items

        Parameters
        ----------
        amount : int
            The number of hitpoints that will be restored up to the maximum number of hitpoints.
        """
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def attack(self, target):
        """A function that allows one entity to attack another
        This function is used when one entity attacks another. Damage is calculated depending on both their stats.
        This function outputs results of such an attack, for example messages to be appended to the messagelog.

        Parameters
        ----------
        target : :obj: `Entity`
            An instance of the entity class. The entity that is to be attacked.
        """
        results = []
        damage = self.power - target.fighter.defense

        if damage > 0:
            results.append({'message': Message('{0} attacks {1}, spraying {2} liters of blood.'.format(
                self.owner.name.capitalize(), target.name, str(damage)), tcod.white)})
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({'message': Message('{0} attacks {1} but does no damage.'.format(
                self.owner.name.capitalize(), target.name),tcod.white)})

        return results