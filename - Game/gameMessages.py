import tcod

import textwrap


class Message:
    """Defines an arbitrary message by text and colour

    Parameters
    ----------
    text : str
        Text to display in the message
    color : tcod.color
        Color to display the message in"""

    def __init__(self, text, color=tcod.white):
        self.text = text
        self.color = color


class MessageLog:
    """Message log object displayed at the bottom of the screen.

    Parameters
    ----------
    x : int
        Starting x-coordinate of messages. (We don't need y because
        it's necessarily set at the bottom of the screen.
    width : int
        Width of message box
    height : int
        Height of message box
    """

    def __init__(self, x, width, height):
        self.messages = []
        self.x = x
        self.width = width
        self.height = height

    def add_message(self, message):
        """Adds a message to the log

        Parameters
        ----------
        message : :obj:`Message`
            The message to display"""
        # Split the message if necessary, among multiple lines
        new_msg_lines = textwrap.wrap(message.text, self.width)

        for line in new_msg_lines:
            # If the buffer is full, remove the first line to make room for the new one
            if len(self.messages) == self.height:
                del self.messages[0]

            # Add the new line as a Message object, with the text and the color
            self.messages.append(Message(line, message.color))