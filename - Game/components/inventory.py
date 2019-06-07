import tcod
from gameMessages import Message

class Inventory:
    """A class that allows an entity to carry items

    This class allows entities to carry items with them, up to a maximum number. This provides the
    necessary functionality for the player to pick up and use items.

    Parameters
    ----------
    capacity : int
        An integer that determines how many items may be carried at maximum by the entity.
    items : list
        A list containing instances of the entity class that are owners of the item class.
        These items are the ones carried by the entity.
    """
    def __init__(self,capacity):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        """A function that allows items to be added to the inventory

        This function allows items to be added to the inventory.
        It is used for example when picking up items off the ground.

        Parameters
        ----------
        item : :obj: `Item`
            An instance of the Item class.
        """
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

    def remove_item(self,item):
        """A function that allows items to be removed from the inventory

        This function allows items to be removed from the inventory.
        It is used for example when using items.

        Parameters
        ----------
        item : :obj: `Item`
            An instance of the Item class.
        """
        self.items.remove(item)

    def use(self, item_entity, **kwargs):
        """A function that allows items in the inventory to be used

        This function allows items to be used.

        Parameters
        ----------
        item_entity : :obj: `Entity`
            An instance of the Entity class that is the owner of an instance of the Item class.
        **kwargs : dict
            A dictionary containing relevant information about what the item can be used for.
            This includes the use_function, for example heal.
            It also includes relevant parameters for such function, for example the amount to be healed.
        """
        results = []
        item_component = item_entity.item

        if item_component.use_function is None:
            results.append({'message': Message('The {0} cannot be used.'.format(item_entity.name), tcod.sky)})
        else:
            kwargs = {**item_component.function_kwargs, **kwargs}
            item_use_results = item_component.use_function(self.owner, **kwargs)

            for item_use_result in item_use_results:
                if item_use_result.get('consumed'):
                    self.remove_item(item_entity)

            results.extend(item_use_results)
        return results