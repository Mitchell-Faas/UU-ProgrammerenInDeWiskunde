import tcod
from gameMessages import Message

class Inventory():
    def __init__(self,capacity):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                'item_added': None,
                'message': Message('You don\'t have room for additional items.')
            })
        else:
            results.append({
                'item_added': item,
                'message': Message('You pick up the {0}!'.format(item.name))
            })

            self.items.append(item)

        return results