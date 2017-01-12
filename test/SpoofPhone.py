
from datetime import datetime
from collections import defaultdict
import emoji

class SpoofPhone():
    """This class provides methods to spoof tools to spoof SMS messages to a Shawk client"""

    def __init__(self, mock_IMAP_instance, sender):
        self.imap = mock_IMAP_instance
        self.sender = sender

    def send(self, messages, time=None, sender=None, emojize=False):
        """Spoof a simple SMS"""

        # Handle arguments
        if not time:
            time = datetime.utcnow()
        if not sender:
            sender = self.sender
        if not isinstance(messages, list):
            messages = [messages]
        if emojize:
            messages = [emoji.emojize(message, use_aliases=True) for message in messages]

        # Spoof IMAP's fetch return value
        self.imap.fetch.return_value = defaultdict(dict)
        message_counter = 1
        for message in messages:
            self.imap.fetch.return_value[message_counter] = {
                b'BODY[TEXT]': str.encode(message),
                b'BODY[HEADER.FIELDS (FROM)]': str.encode(sender.get_address()),
                b'INTERNALDATE': str.encode(str(time))
            }
