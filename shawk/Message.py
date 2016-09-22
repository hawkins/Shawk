
class Message():
    def __init__(self, text, sender, date=None):
        self.sender = sender
        self.text = str(text).strip()
        self.date = date

    def __repr__(self):
        return "<shawk.Message('{}', '{}', '{}')>".format(self.sender, self.text)

    def __str__(self):
        return "Message from {} at {}: \"{}\"".format(str(self.sender), self.date, self.text)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False
