
class Message():
    def __init__(self, text, sender):
        self.sender = sender
        self.text = str(text)

    def __repr__(self):
        return "<shawk.Message('{}', '{}', '{}')>".format(self.sender, self.text)

    def __str__(self):
        return "From {}: {}".format(str(self.sender), self.text)
