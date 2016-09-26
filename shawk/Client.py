"""
shawk.Client
------------

Define the Client interface in Shawk.
"""

from __future__ import print_function
from threading import Timer
import email
import re
import smtplib
import imapclient
from shawk.Contact import Contact
from shawk.Message import Message
from shawk import SMS_Address_Regex, sms_to_mail

class Client(object):
    """Define the main Shawk interface."""

    def __init__(self, user, pwd, inbox=True, auto=True, handler=None):
        """
        Initialize the client and configure SMTP for sending messages.

        This will establish an SMTP connection for sending messages to contacts.
        Note that each instance of Client should be configured to a unique user (email).
        """

        self.__user = user
        self.contacts = {}
        self.inbox = []
        self.latest_messages = []
        self.auto_refresh_enabled = auto
        self.refresh_interval = 10 # Time in seconds

        # Configure SMTP

        self.smtp = smtplib.SMTP("smtp.gmail.com", 587)
        self.smtp.starttls()
        self.smtp.login(str(user), str(pwd))

        # Handle optional arguments

        if handler:
            self.handler = handler
        else:
            self.handler = lambda x: print('Shawk received message: %s' % x)

        if inbox:
            self.setup_inbox(pwd, auto=self.auto_refresh_enabled)

    def __repr__(self):
        """Return the object representation of the Client."""

        return "<shawk.Client({})>".format(self.__user)

    def __str__(self):
        """Return the String representation of the Client."""

        return "A Shawk SMS Client for {}".format(self.__user)

    def __del__(self):
        """Delete the object."""

        self.smtp.quit()
        try:
            self.imap.logout()
        except AttributeError:
            pass

    def add_contact(self, number, carrier, name=None):
        """
        Create a new Contact instance and add to contacts.

        You can also pass a list of numbers, carriers, and names to create multiple at once.
        """
        # If the two are lists, add each to the contacts
        if isinstance(number, list) and isinstance(carrier, list):
            # Ensure name is also list
            if name and not isinstance(name, list):
                raise Exception("Not enough names")

            if name:
                self.contacts.update({str(nu): Contact(nu, ca, na) for (nu, ca, na) in (number, carrier, name)})
            else:
                self.contacts.update({str(nu): Contact(nu, ca) for (nu, ca) in (number, carrier)})

        # Add the number and carrier to contacts if single pair is provided
        if name:
            self.contacts.update({str(number): Contact(number, carrier, name)})
        else:
            self.contacts.update({str(number): Contact(number, carrier)})

    def remove_contact(self, contact=None, number=None, name=None):
        """Remove a contact from contacts."""

        if not number and not name and not contact:
            raise Exception("No identifier provided")

        # Find number

        # Check contact
        if contact and not number:
            number = contact.get_number()

        # Check name
        if not number:
            for each in self.contacts:
                if each.name == name:
                    number = each.number
                    break

        # Raise exception if not found
        if not number:
            raise Exception("No matching contact found")

        # Delete the object from contacts
        del self.contacts[str(number)]

    def get_contact(self, message):
        """
        Return the Contact from a given message's sender.

        Returns None if sender not in contacts.
        """

        # Return contact that matches the message's sender
        address = message.get_address()
        for _, contact in self.contacts.items():
            if contact.get_address() == address:
                return contact
        return None

    def get_contact_from_address(self, address):
        """
        Return the Contact matching a given address.

        Returns None if not in contacts.
        """

        # Return contact that matches an address
        for _, contact in self.contacts.items():
            if contact.get_address() == address:
                return contact
        return None

    def setup_inbox(self, password, user=None, folder='INBOX', refresh=False, auto=False, ssl=True):
        """
        Configure an IMAP connection for receiving SMS.

        Optionally configure behaviours such as auto-refresh,
        refresh immediately once configured, or specify a folder.

        Folder specifications are useful if you configure your Gmail account to
        filter messages from certain senders to be moved to a specific folder,
        that way they don't clutter your Gmail Inbox folder.
        """

        # Apply user if not provided
        if not user:
            user = self.__user

        # Connect IMAP server
        self.imap = imapclient.IMAPClient('imap.gmail.com', ssl=ssl)
        self.imap.login(user, password)
        self.imap.select_folder(folder, readonly=True)

        # Refresh if requested
        if refresh and not auto:
            self.refresh()
        if auto:
            self.enable_auto_refresh()
            self.auto_refresh()

    def enable_auto_refresh(self, start=True):
        """
        Enable auto refresh of inbox.

        Will also begin refreshing now, but can be disabled with `start=False`.
        """

        self.auto_refresh_enabled = True

        if start:
            self.auto_refresh()

    def disable_auto_refresh(self):
        """Disable auto refresh of inbox."""

        self.auto_refresh_enabled = False

    def auto_refresh(self):
        """Refresh the inbox automatically on an interval."""

        if self.auto_refresh_enabled:
            if self.imap:
                self.refresh()
                Timer(self.refresh_interval, self.auto_refresh, ()).start()
            else:
                raise Exception("No inbox is setup")

    def refresh(self):
        """Refresh the inbox only once."""

        # Get raw messages from imap
        uids = self.imap.search('ALL')
        raw_msgs = self.imap.fetch(uids, ['BODY[TEXT]', 'BODY[HEADER.FIELDS (FROM)]', 'INTERNALDATE'])

        # Convert messages to string format and simplify structure
        messages = []
        for uid in raw_msgs:
            obj = {}
            obj['UID'] = uid
            for key, value in raw_msgs[uid].items():
                try:
                    if key.decode('utf-8') == 'BODY[HEADER.FIELDS (FROM)]':
                        obj['FROM'] = email.utils.parseaddr(value.decode('utf-8'))[1]
                    else:
                        if key.decode('utf-8') == 'BODY[TEXT]':
                            obj['BODY'] = value.decode('utf-8')
                        else:
                            obj[key.decode('utf-8')] = value.decode('utf-8')
                except AttributeError:
                    obj[key.decode('utf-8')] = value
            messages.append(obj)

        # Find sms messages in messages
        self.latest_messages = []
        for msg in messages:

            # If the sender's email address is in our supported gateways
            if re.match(SMS_Address_Regex, msg['FROM']):

                # Create Message object
                contact = self.get_contact_from_address(msg['FROM'])
                new_msg = Message(msg['BODY'], (contact or msg['FROM']), msg['INTERNALDATE'])

                # Add to inbox and latest_messages
                if new_msg not in self.inbox:
                    self.latest_messages.append(new_msg)
                    self.inbox.append(new_msg)

        # Handle the new texts
        for text in self.latest_messages:
            self.handler(self, text)

    def set_refresh_interval(self, time):
        """Define the refresh interval for auto refresh."""

        self.refresh_interval = time

    def get_refresh_interval(self):
        """Return the refresh interval for auto refresh."""

        return self.refresh_interval

    def set_handler(self, func):
        """Set the handler function callback for new messages."""

        self.handler = func

    def __sendmail(self, address, message):
        """Send the content of message to address."""

        return self.smtp.sendmail('0', address, message)

    def send(self, message, contact=None, address=None, number=None, name=None, carrier=None):
        """
        Send a message.

        Can determine a contact to use via a number of different specifications,
        but it is advised to specify a Contact object if possible.

        However, passing a specific address takes precedence over any other input.
        """

        if not contact and not name and not number and not address:
            raise Exception("No contact information provided")

        # Convert Message instances to string
        if isinstance(message, Message):
            message = message.text

        # Send message to recipient
        if address:
            return self.__sendmail(address, message)
        if contact:
            return self.__sendmail(contact.get_address(), message)

        # Address is not readily available, determine from other inputs

        # Find address if given number
        if number:
            number = str(number)

            # Get address of recipient
            try:
                address = self.contacts[number].get_address()
                return self.__sendmail(address, message)
            except KeyError:
                # Number not in contacts
                if not carrier:
                    # Not enough information
                    raise Exception("Could not find number {} in contacts; require carrier information".format(number))
                else:
                    # Build address
                    address = sms_to_mail(number, carrier)
                    # Send the message
                    return self.__sendmail(address, message)

        # Find address if only given name
        if name and not address:
            name = str(name)
            for _, each in self.contacts.items():
                if each.name == name:
                    address = each.get_address()

                    # Send the message
                    return self.__sendmail(address, message)

            if not number:
                # Name was not found in contacts
                raise Exception("No contact found matching the name {}".format(name))
