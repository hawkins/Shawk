"""
shawk.Message
-------------

Define the Message representation in Shawk.
"""

class Message(object):
    """Define the structure for messages."""

    def __init__(self, text, sender, date=None):
        """Initialize a Message."""

        self.text = str(text).strip()
        self.sender = sender
        self.date = date

    def __repr__(self):
        """Return the object representation of the Message."""

        if self.date:
            return "<shawk.Message('{}', '{}', '{}')>".format(self.text, self.sender, self.date)
        else:
            return "<shawk.Message('{}', '{}')>".format(self.text, self.sender)

    def __str__(self):
        """Return the String representation of the Message."""

        return "Message from {} at {}: \"{}\"".format(str(self.sender), self.date, self.text)

    def __eq__(self, other):
        """Determine if one Message is equivalent to another."""

        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False
