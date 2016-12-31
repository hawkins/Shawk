"""
shawk.Client
------------

Define the Client interface in Shawk.
"""

from __future__ import print_function
from threading import Thread
from time import sleep
import re
import csv
import email
import emoji
import smtplib
import imapclient

from shawk.Contact import Contact
from shawk.Message import Message
from shawk import SMS_Address_Regex, sms_to_mail

class Client(object):
    """Client is the main Shawk interface"""

    def __init__(self, user, password, emojize=True, demojize=True):
        """
        Initialize the client and configure SMTP for sending messages.

        This will establish an SMTP connection for sending messages to contacts.
        Note that each instance of Client should be configured to a unique user (email).
        """

        self.__user = user
        self.contacts = {}
        self.inbox = []
        self.latest_messages = []
        self.processed_label = "[Shawk]/Processed"
        self.refresh_interval = 0 # Time in seconds
        self.auto_refresh_enabled = False
        self.text_handlers = {}
        self.contact_handlers = {}
        self.emojize = emojize
        self.demojize = demojize

        # Configure SMTP
        self.setup_outbox("smtp.gmail.com", 587, user, password)

    def __repr__(self):
        """Return the object representation of the Client"""

        return "<shawk.Client({})>".format(self.__user)

    def __str__(self):
        """Return the String representation of the Client"""

        return "A Shawk SMS Client for {}".format(self.__user)

    def __del__(self):
        """Delete the object"""

        self.smtp.quit()
        try:
            self.imap.logout()
        except AttributeError:
            pass

    def add_contact(self, number, carrier, name=None):
        """
        Create a new Contact instance and add to contacts.

        Returns the created Contact instance.
        """

        # Add the number and carrier to contacts
        if name:
            self.contacts.update({str(number): Contact(number, carrier, name)})
        else:
            self.contacts.update({str(number): Contact(number, carrier)})

        # Return the Contact
        return self.contacts[str(number)]

    def remove_contact(self, contact=None, number=None, name=None):
        """Remove a contact from contacts"""

        if not number and not name and not contact:
            raise Exception("No identifier provided")

        # Find number

        # Check contact
        if contact and not number:
            number = contact.get_number()

        # Check name
        if not number:
            for _, c in self.contacts.items():
                if c.get_name() == name:
                    number = c.get_number()
                    break

        # Raise exception if number not found
        if not number:
            raise Exception("No matching contact found")

        # Remove any contact_handlers for this Contact
        if self.contacts[str(number)] in self.contact_handlers.keys():
            del self.contact_handlers[self.contacts[str(number)]]

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

    def set_processed_label(self, label):
        """Set the processed message label to store messages in"""

        self.processed_label = label

    def __mark_uid_processed(self, uid):
        """Set this email's label to processed_label"""

        # Move uid to folder
        self.imap.copy(uid, self.processed_label)
        self.imap.delete_messages(uid)

    def setup_outbox(self, host, port, user, password):
        """Configure an SMTP connection for sending SMS"""

        self.smtp = smtplib.SMTP(host, port)
        self.smtp.starttls()
        self.smtp.login(str(user), str(password))

    def setup_inbox(self, password, user=None, folder='INBOX', refresh=False, auto=False, ssl=True):
        """
        Configure an IMAP connection for receiving SMS.

        Optionally configure behaviours such as auto-refresh,
        refresh immediately once configured, or specify a folder.

        This method will also attempt to create a folder/label in your
        Gmail account to store processed messages in.

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
        self.imap.select_folder(folder)

        # Create processed folder
        if not self.imap.folder_exists(self.processed_label):
            self.imap.create_folder(self.processed_label)

        # Refresh if requested
        if refresh and not auto:
            self.refresh()
        elif auto:
            self.enable_auto_refresh(start=True)

    def enable_auto_refresh(self, start=True, verbose=False):
        """
        Enable auto refresh of inbox

        Will also begin refreshing now, but can be disabled with `start=False`.

        Can optionally log information about each refresh with `verbose=True`.
        """

        self.auto_refresh_enabled = True

        if start:
            self.__auto_refresh(verbose)

    def disable_auto_refresh(self):
        """Disable auto refresh of inbox"""

        self.auto_refresh_enabled = False

    def __auto_refresh(self, verbose):
        """Refresh the inbox automatically on an interval"""

        # If email inbox is configured
        if self.imap:
            # Start daemon thread
            self.thread = Thread(target=self.__daemon, args=(verbose,))
            self.thread.daemon = True
            self.thread.start()
        else:
             raise Exception("No inbox is setup")

    def __daemon(self, verbose):
        """Runs in background to refresh periodically until autO_refresh is disabled"""

        # Run until no longer enabled
        while self.auto_refresh_enabled:
            self.refresh(verbose)

            sleep(self.refresh_interval)

    def refresh(self, verbose=False):
        """
        Refresh the inbox only once

        Optionally log with `verbose=True`
        """

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
                if self.demojize:
                    new_msg = Message(emoji.demojize(msg['BODY']), (contact or msg['FROM']), msg['INTERNALDATE'])
                else:
                    new_msg = Message(msg['BODY'], (contact or msg['FROM']), msg['INTERNALDATE'])

                # Track message uid
                new_msg.uid = msg['UID']

                # If this message is new
                if new_msg not in self.inbox:

                    # Add to inbox and latest_messages
                    self.latest_messages.append(new_msg)
                    self.inbox.append(new_msg)

        # Handle the new texts
        for msg in self.latest_messages:
            # Keep track of whether a specific handler has matched this text or not
            matched_handler = False

            # Consider contact handlers first

            # Ensure we have a contact
            if isinstance(msg.sender, Contact):
                # If specific handlers did exist for this contact
                if msg.sender in self.contact_handlers.keys():
                    # If there is a handler attached
                    if len(self.contact_handlers[msg.sender]) > 0:
                        matched_handler = True

                    # Call all of its functions
                    for func in self.contact_handlers[msg.sender]:
                        func(self, msg)

            # Now consider text handlers

            # For each regex and function in text_handlers
            for regex, functions in self.text_handlers.items():
                # Execute regex on the text
                match = regex.match(msg.text)

                # If a match occurred, call the functions attached to it
                if match:
                    # If there are still any functions attached
                    if len(functions) > 0:
                        matched_handler = True

                    # Call all of them
                    for func in functions:
                        func(self, msg, match, regex)

            # If we did not match any specific handler
            if not matched_handler:

                # Execute default text handler
                self.default_text_handler(self, msg)

            # Move message to processed_label
            self.__mark_uid_processed(msg.uid)

        # Log if requested
        if verbose:
            print("Found {} new messages".format(len(self.latest_messages)))

    def set_refresh_interval(self, interval):
        """Define the refresh interval for auto refresh"""

        self.refresh_interval = interval

    def get_refresh_interval(self):
        """Return the refresh interval for auto refresh"""

        return self.refresh_interval

    def default_text_handler(self, client, message):
        """
        This is the default text handler provided by Shawk.

        If self.demojize is True, this converts emoji to text and prints the message.
        Otherwise, this simply prints the raw message text.
        """

        greeting = "Shawk received message"

        if self.demojize:
            demojized_text = emoji.demojize(message.text)
            print("{}: {}".format(greeting, demojized_text))
        else:
            print("{}: {}".format(greeting, message.text))

    def text_handler(self, pattern=None, modifiers=''):
        """
        Define a decorator that accepts a regular expression in string form for handlers.

        Sets the default text handler if no string is provided.
        """

        if pattern:
            # Collect modifiers
            modifiers = modifiers.lower()
            flags = 0
            if 's' in modifiers:
                flags = re.DOTALL     if not flags else flags | re.DOTALL
            if 'i' in modifiers:
                flags = re.IGNORECASE if not flags else flags | re.IGNORECASE
            if 'm' in modifiers:
                flags = re.MULTILINE  if not flags else flags | re.MULTILINE
            if 'l' in modifiers:
                flags = re.LOCALE     if not flags else flags | re.LOCALE
            if 'u' in modifiers:
                flags = re.UNICODE    if not flags else flags | re.UNICODE
            if 'x' in modifiers:
                flags = re.VERBOSE    if not flags else flags | re.VERBOSE

            # Compile the regular expression
            try:
                text_regex = re.compile(pattern, flags)
            except Exception as e:
                raise Exception("An error occured while compiling regex: ", e)

        def decorator(func):
            """Closure that receives function"""

            # Set the default text handler if no regex is provided
            if not pattern:
                self.set_default_text_handler(func)
            else:
                # Add to text_handlers
                self.add_text_handler(text_regex, func)

            # Return unmodified function
            return func

        # Return decorator
        return decorator

    def contact_handler(self, contact):
        """
        Define a decorator that accepts a shawk.Contact object to define contact_handler.

        Sets the default text handler if no string is provided.
        """

        def decorator(func):
            """Closure that receives function"""

            # Add to contact_handlers
            self.add_contact_handler(contact, func)

            # Return unmodified function
            return func

        # Return decorator
        return decorator

    def set_default_text_handler(self, handler):
        """Set the default text handler to the given handler function"""

        self.default_text_handler = handler

    def add_text_handler(self, regex, handler):
        """Associate a given handler to the given compiled regex"""

        # Add to existing list or initialize list
        if regex in self.text_handlers.keys():
            self.text_handlers[regex].append(handler)
        else:
            self.text_handlers[regex] = [handler]

    def remove_text_handler(self, regex, handler):
        """Removes a given handler from the given compiled regex"""

        # If this regex has a handler
        if regex in self.text_handlers.keys():
            self.text_handlers[regex].remove(handler)

    def add_contact_handler(self, contact, handler):
        """Associate a given handler to the contact"""

        # Add to existing list or initialize list
        if contact in self.contact_handlers.keys():
            self.contact_handlers[contact].append(handler)
        else:
            self.contact_handlers[contact] = [handler]

    def remove_contact_handler(self, contact, handler):
        """Removes a given handler given its contact"""

        # If this contact has a contact_handler
        if contact in self.contact_handlers.keys():
            self.contact_handlers[contact].remove(handler)

    def export_contacts(self, path):
        """Export the current contacts to a Shawk CSV file"""

        # Open path to overwrite
        with open(path, 'w') as outcsv:
            writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            # Add version specific formatting
            writer.writerow(['Shawk contacts file', 'v', '0.4'])
            # Add each contact's information
            for _, contact in self.contacts.items():
                writer.writerow([contact.get_number(), contact.get_carrier(), contact.get_name()])

    def import_contacts(self, path):
        """Import contacts from a Shawk CSV file"""

        # In the future, we'll depend on csv_version to handle differences in file format
        csv_version = ''

        # Open path to read
        with open(path, 'r') as incsv:
            reader = csv.reader(incsv, delimiter=',', quotechar='|')
            first_row = next(reader)
            if first_row[0] == 'Shawk contacts file' and first_row[1] == 'v':
                csv_version = first_row[2]
            for row in reader:
                self.contacts[row[0]] = Contact(number=row[0], carrier=row[1], name=row[2])

    def print_contacts(self):
        """Print the contacts"""

        for _, contact in self.contacts.items():
            print(contact)

    def __sendmail(self, address, text):
        """Send the content of message to address"""

        if self.emojize:
            text = emoji.emojize(text, use_aliases=True)

        return self.smtp.sendmail('0', address, text)


    def send(self, message, contact=None, address=None, number=None, name=None, carrier=None):
        """
        Send a message.

        Can determine a contact to use via a number of different specifications,
        but it is advised to specify a Contact object if possible.

        However, passing a specific address takes precedence over any other input.
        """

        if not contact and not name and not number and not address:
            raise Exception("No contact information provided")

        if contact:
            assert(type(contact) is Contact)

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
