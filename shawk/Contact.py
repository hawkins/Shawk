"""
shawk.Contact
-------------

Define the Contact representation in Shawk.
"""

from shawk import Gateways, sms_to_mail

class Contact(object):
    """Define the structure for contacts."""

    def __init__(self, number, carrier, name=None):
        """Initialize a Contact."""

        self.name = name
        self.number = str(number)
        self.carrier = carrier

    def __repr__(self):
        """Return the object representation of the Contact."""

        return "<shawk.Contact('{}', '{}', '{}')>".format(self.number, self.carrier, self.name if self.name else '<No name>')

    def __str__(self):
        """Return the String representation of the Contact."""

        return "{}: {} ({})".format(self.name if self.name else '<No name>', self.number, self.carrier)

    def get_address(self):
        """Return the email address of the Contact."""

        return sms_to_mail(self.number, self.carrier)

    def get_number(self):
        """Return the number of the Contact."""

        return self.number

    def get_carrier(self):
        """Return the carrier of the Contact."""

        return self.carrier

    def get_name(self):
        """Return the name of the Contact."""

        return self.name

