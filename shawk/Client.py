from __future__ import print_function
from shawk.Contact import Contact
from shawk.Message import Message
from threading import Timer
import smtplib
import imapclient # Version 0.13
import email

class Client():
    def __init__(self, user, pwd):
        self.__user = user
        self.contacts = {}
        self.smtp = smtplib.SMTP("smtp.gmail.com", 587)
        self.smtp.starttls()
        self.smtp.login(str(user), str(pwd))
        self.inbox = []
        self.latestMessages = []
        self.autoRefreshEnabled = False
        self.refreshInterval = 10 # Time in seconds
        self.handler = lambda x: print('Shawk received message: %s' % x)

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

        # Delete the object from contacts
        del self.contacts[str(number)]

    def getContact(self, message):
        # Return contact that matches the message's sender
        for _, contact in self.contacts.items():
            if contact.getAddress() == message['FROM']:
                return contact
        return None

    def getContactFromAddress(self, address):
        # Return contact that matches an address
        for _, contact in self.contacts.items():
            if contact.getAddress() == address:
                return contact
        return None

    def setupInbox(self, password, folder='inbox', user=None, refresh=False, auto=False):
        # Apply user if not provided
        if not user:
            user = self.__user

        # Connect IMAP server
        self.imap_server = imapclient.IMAPClient('imap.gmail.com', ssl=True)
        self.imap_server.login(user, password)
        self.imap_server.select_folder('INBOX', readonly=True)

        # Refresh if requested
        if refresh and not auto:
            self.refreshInbox()
        if auto:
            self.enableAutoRefresh()
            self.refreshAutomatically()

    def enableAutoRefresh(self):
        self.autoRefreshEnabled = True

    def disableAutoRefresh(self):
        self.autoRefreshEnabled = False

    def refreshAutomatically(self):
        if self.autoRefreshEnabled:
            if self.imap_server:
                self.refreshInbox()
                Timer(self.refreshInterval, self.refreshAutomatically, ()).start()
            else:
                raise Exception("No inbox is setup")

    def refreshInbox(self):
        # Get raw messages from imap_server
        UIDs = self.imap_server.search('ALL')
        rawMessages = self.imap_server.fetch(UIDs, ['BODY[TEXT]', 'BODY[HEADER.FIELDS (FROM)]', 'INTERNALDATE'])

        # Convert messages to string format and simplify structure
        messages = []
        for uid in rawMessages:
            obj = {}
            obj['UID'] = uid
            for key, value in rawMessages[uid].items():
                try:
                    if key.decode('utf-8') == 'BODY[HEADER.FIELDS (FROM)]':
                        obj['FROM'] = email.utils.parseaddr(value.decode('utf-8'))[1]
                    else:
                        if key.decode('utf-8') == 'BODY[TEXT]':
                            obj['BODY'] = value.decode('utf-8')
                        else:
                            obj[key.decode('utf-8')] = value.decode('utf-8')
                except AttributeError as e:
                    obj[key.decode('utf-8')] = value
            messages.append(obj)

        # Find sms messages in messages
        # TODO: Look for sender matching a Contact's address
        self.latestMessages = []
        for msg in messages:
            content = msg['BODY']
            if len(content) < 140:
                # Create Message object
                contact = self.getContactFromAddress(msg['FROM'])
                newMessage = Message(msg['BODY'], (contact or msg['FROM']), msg['INTERNALDATE'])

                # Add to inbox and latestMessages
                if newMessage not in self.inbox:
                    self.latestMessages.append(newMessage)
                    self.inbox.append(newMessage)

        # Handle the new texts
        for text in self.latestMessages:
            self.handler(text)

    def setRefreshInterval(self, time):
        self.refreshInterval = time

    def getRefreshInterval(self, time):
        return self.refreshInterval

    def setHandler(self, func):
        self.handler = func

    def send(self, message, contact=None, number=None, name=None, carrier=None):
        if not contact and not name and not number:
            raise Exception("No contact information provided")

        if isinstance(message, Message):
            message = message.text

        address = None

        # Find address from contact
        if contact:
            address = contact.getAddress()

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
