class Item:
    """A class that can be used when creating an entity, to make it into an item

    When creating an instance of the entity class, it can be handed an instance of this class to give it the
    properties of an item. This means it can be picked up, carried in an inventory, and possible used.

    Parameters
    ----------
    use_function : function, optional
        The use_function allows us to define whether an item is usable, and if so, what its effect is.
        An example is the item_heal function, which heals the user.
    **kwargs
        Keyword arguments to pass on to the usage function.
        An example is the amount healed with the item_heal function.
    """
    def __init__(self, use_function = None, **kwargs):
        self.use_function = use_function
        self.function_kwargs = kwargs