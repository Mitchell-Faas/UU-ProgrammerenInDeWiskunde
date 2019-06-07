import tcod


class BasicMonster:
    """A class that can be used when creating enemy entity instances, to allow them to take basic actions
    This class can be optionally given to an entity. If this class is given to an entity,
    it will be able to move and make attacks when in view of the player.
    """
    def take_turn(self, target, fov_map, game_map, entities):
        """A function that lets enemies take their turn

        This function is called to let enemies take their turn. If they are in view of the player, they will attack
        if they can, or otherwise move towards the player. The function outputs the result of any such action
        where necessary, such as messages to be put in the message log.

        Parameters
        ----------
        target : :obj:`Entity`
            The target entity to be attacked. Currently this is always the player.
        fov_map : :obj:`TCODMap`
            A map-object from the tcod library. It keeps track of which tiles are visible.
            If a monster is outside player vision, it does not act.
        game_map : :obj:`GameMap`
            A class for the game-map. It includes information about which tiles can be walked through.
            This is necessary information for path-finding by enemies.
        entities : list
            A list of instances of the entity class. This is necessary for path-finding because
            monsters cannot move through each other.
        """
        results = []

        monster = self.owner
        if tcod.map_is_in_fov(fov_map, monster.x, monster.y):
            if monster.distance_to(target) >= 2:
                monster.move_astar(target, entities, game_map)
            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)

            return results
