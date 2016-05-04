from shawk.Contact import Contact
import smtplib

class Client():
    def __init__(self, user, pwd):
        self.__user = user
        self.contacts = {}
        self.smtp = smtplib.SMTP("smtp.gmail.com", 587)
        self.smtp.starttls()
        self.smtp.login(str(user), str(pwd))

    def __repr__(self):
        return "<shawk.Client()>"

    def __str__(self):
        return "A Shawk SMS Client for {}".format(self.__user)

    def __del__(self):
        self.smtp.quit()

    def addContact(self, number, carrier, name=None):
        # If the two are lists, add each to the contacts
        if isinstance(number, list) and isinstance(carrier, list):
            # Ensure name is also list
            if name and not isinstance(name, list):
                raise Exception("Not enough names")
                return

            if name:
                self.contacts.update({str(nu): Contact(nu, ca, na) for (nu, ca, na) in (number, carrier, name)})
            else:
                self.contacts.update({str(nu): Contact(nu, ca) for (nu, ca) in (number, carrier)})

        # Add the number and carrier to contacts if single pair is provided
        if name:
            self.contacts.update({str(number): Contact(number, carrier, name)})
        else:
            self.contacts.update({str(number): Contact(number, carrier)})

    def removeContact(self, number=None, name=None):
        if not number and not name:
            raise Exception("No identifier provided")

        # Find number if not provided
        if not number:
            name = str(name)
            for each in self.contacts:
                if each.name == name:
                    number = each.number
                    break

        del self.contacts[str(number)]

    def send(self, message, name=None, number=None, carrier=None):
        if not name and not number:
            raise Exception("No name or number provided")

        address = None

        # Find address if given number
        if number:
            # Ensure number is a string
            number = str(number)

            # Get address of recipient
            try:
                address = self.contacts[number].getAddress()
            except:
                # Number not in contacts
                if not carrier:
                    # Not enough information
                    raise Exception("Could not find number in contacts; require carrier information")
                else:
                    # Add it to contacts
                    self.contacts.update({number: Contact(number, carrier)})
                    address = self.contacts[number].getAddress()

        # Find address if only given name
        if name and not address:
            name = str(name)
            for key, each in self.contacts.items():
                if each.name == name:
                    address = each.getAddress()
                    break
            if not number:
                # Name was not found in contacts
                raise Exception("No contact found matching the name {}".format(name))

        # Send message to recipient
        if address:
            self.smtp.sendmail('0', address, message)
