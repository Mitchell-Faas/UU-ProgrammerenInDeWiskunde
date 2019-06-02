import tcod
from gameMessages import Message

def item_heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'consumed': False, 'message': Message('Your veins already flow with ample blood.', tcod.sky)})
    else:
        entity.fighter.heal(amount)
        results.append({'consumed': True, 'message': Message('You ingest the blood. Your pain diminishes.', tcod.green)})

    return results