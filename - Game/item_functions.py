import tcod
from gameMessages import Message

def item_heal(entity, amount):
    """Executes the actions associated with healing items

    Parameters
    ----------
    entity : :obj:`Entity`
        Entity to heal
    amount : int
        Amount to heal the entity

    Returns
    -------
    list
        List containing the dict entry to add to
        player_results in engine."""

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'consumed': False, 'message': Message('Your veins already flow with ample blood.', tcod.sky)})
    else:
        entity.fighter.heal(amount)
        results.append({'consumed': True, 'message': Message('You ingest the blood. Your pain diminishes.', tcod.green)})

    return results