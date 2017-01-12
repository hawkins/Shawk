
from mock import patch, call
from copy import deepcopy
from time import sleep
from datetime import datetime
import re
import emoji

import shawk
from test import SpoofPhone

# Prepare client variables
username = 'username@email.com'
password = 'password'

#
# Test adding and removing contacts
#

@patch('smtplib.SMTP')
def test_creating_a_client(mock_SMTP):
    """Test creating a client"""

    client = shawk.Client(username, password)

    assert(type(client) == shawk.Client)
    assert(str(client) == 'A Shawk SMS Client for username@email.com')

@patch('smtplib.SMTP')
def test_add_contact_minimal(mock_SMTP):
    """Test adding a contact without a name"""

    client = shawk.Client(username, password)
    contacts_before = deepcopy(client.contacts)

    client.add_contact(number=1234567890, carrier='Verizon')
    contacts_after = client.contacts

    assert(contacts_before != contacts_after)
    assert(str(contacts_after) == "{'1234567890': <shawk.Contact('1234567890', 'Verizon', '<No name>')>}")

@patch('smtplib.SMTP')
def test_add_contact_with_name(mock_SMTP):
    """Test adding a contact with a name"""

    client = shawk.Client(username, password)
    contacts_before = deepcopy(client.contacts)

    client.add_contact(number=1234567890, carrier='Verizon', name='Somebody')
    contacts_after = client.contacts

    assert(contacts_before != contacts_after)
    assert(str(contacts_after) == "{'1234567890': <shawk.Contact('1234567890', 'Verizon', 'Somebody')>}")

@patch('smtplib.SMTP')
def test_remove_contact_by_number(mock_SMTP):
    """Test removing a contact by specifying its number"""

    client = shawk.Client(username, password)
    client.add_contact(number=1234567890, carrier='Verizon')
    contacts_before = deepcopy(client.contacts)

    client.remove_contact(number=1234567890)
    contacts_after = client.contacts

    assert(contacts_before != contacts_after)
    assert(contacts_after == {})

@patch('smtplib.SMTP')
def test_remove_contact_by_name(mock_SMTP):
    """Test removing a contact by specifying its name"""

    client = shawk.Client(username, password)
    client.add_contact(number=1234567890, carrier='Verizon', name='Somebody')
    contacts_before = deepcopy(client.contacts)

    client.remove_contact(name='Somebody')
    contacts_after = client.contacts

    assert(contacts_before != contacts_after)
    assert(contacts_after == {})

@patch('smtplib.SMTP')
def test_remove_contact_by_contact(mock_SMTP):
    """Test removing a contact by specifying its Contact"""

    client = shawk.Client(username, password)
    contact = client.add_contact(number=1234567890, carrier='Verizon', name='Somebody')
    contacts_before = deepcopy(client.contacts)

    client.remove_contact(contact=contact)
    contacts_after = client.contacts

    assert(contacts_before != contacts_after)
    assert(contacts_after == {})

#
# Test sending messages
#

@patch('smtplib.SMTP')
def test_send_message_by_contact(mock_SMTP):
    """Test sending a message to a Contact"""

    client = shawk.Client(username, password)
    contact = client.add_contact(number=1234567890, carrier='Verizon', name='Somebody')
    address = contact.get_address()
    message = 'Testing'

    client.send(message, contact=contact)
    instance = mock_SMTP.return_value

    assert(instance.sendmail.call_count == 1)
    assert(instance.sendmail.mock_calls == [call('0', address, message)])

@patch('smtplib.SMTP')
def test_send_message_by_number(mock_SMTP):
    """Test sending a message to a number"""

    client = shawk.Client(username, password)
    number = 1234567890
    contact = client.add_contact(number=number, carrier='Verizon', name='Somebody')
    address = contact.get_address()
    message = 'Testing'

    client.send(message, number=number)
    instance = mock_SMTP.return_value

    assert(instance.sendmail.call_count == 1)
    assert(instance.sendmail.mock_calls == [call('0', address, message)])

@patch('smtplib.SMTP')
def test_send_message_by_namer(mock_SMTP):
    """Test sending a message to a name"""

    client = shawk.Client(username, password)
    name = 'Somebody'
    contact = client.add_contact(number=1234567890, carrier='Verizon', name=name)
    address = contact.get_address()
    message = 'Testing'

    client.send(message, name=name)
    instance = mock_SMTP.return_value

    assert(instance.sendmail.call_count == 1)
    assert(instance.sendmail.mock_calls == [call('0', address, message)])

@patch('smtplib.SMTP')
def test_send_message_by_address(mock_SMTP):
    """Test sending a message to an address"""

    client = shawk.Client(username, password)
    contact = client.add_contact(number=1234567890, carrier='Verizon', name='Somebody')
    address = contact.get_address()
    message = 'Testing'

    client.send(message, address=address)
    instance = mock_SMTP.return_value

    assert(instance.sendmail.call_count == 1)
    assert(instance.sendmail.mock_calls == [call('0', address, message)])

#
# Test receiving messages
#

@patch('smtplib.SMTP')
@patch('imapclient.IMAPClient')
def test_receiving_messages_manually(mock_IMAP, mock_SMTP):
    """Test receiving a simple text message"""

    client = shawk.Client(username, password)
    client.setup_inbox(password)
    imap_instance = client.imap
    spoof_contact = client.add_contact(number=1234567890, carrier='Verizon', name='Spoof')
    spoof_phone = SpoofPhone(imap_instance, spoof_contact)
    message_time = datetime.utcnow()
    spoof_phone.send('Testing', message_time)

    client.refresh()

    assert(imap_instance.copy.call_count == 1)
    assert(str(client.inbox) == str([shawk.Message('Testing', spoof_phone.sender, message_time)]))

@patch('smtplib.SMTP')
@patch('imapclient.IMAPClient')
def test_receiving_messages_automatically(mock_IMAP, mock_SMTP):
    """Test receiving a simple text message automatically"""

    client = shawk.Client(username, password)
    client.setup_inbox(password, auto=True)
    imap_instance = client.imap
    spoof_contact = client.add_contact(number=1234567890, carrier='Verizon', name='Spoof')
    spoof_phone = SpoofPhone(imap_instance, spoof_contact)
    message_time = datetime.utcnow()
    spoof_phone.send('Testing', message_time)

    # TODO: How best should we wait for this?
    sleep(max(3, 2 * client.refresh_interval))

    assert(imap_instance.copy.call_count == 1)
    assert(str(client.inbox) == str([shawk.Message('Testing', spoof_phone.sender, message_time)]))

#
# Test text handler functions
#

@patch('smtplib.SMTP')
@patch('imapclient.IMAPClient')
def test_adding_default_text_handler_via_decorator(mock_IMAP, mock_SMTP):
    """Test adding a default text handler and verify that it replaces the stock handler"""

    client = shawk.Client(username, password)
    client.setup_inbox(password)
    spoof_contact = client.add_contact(number=1234567890, carrier='Verizon', name='Spoof')
    spoof_phone = SpoofPhone(client.imap, spoof_contact)
    context = {} # HACK: Ugly way to avoid closure non-local scope issues in Python 2

    @client.text_handler()
    def decorated_default_text_handler(client, message):
        context['did_call_decorated_default_text_handler'] = True

    spoof_phone.send('Testing')
    client.refresh()

    assert(context['did_call_decorated_default_text_handler'])

@patch('smtplib.SMTP')
@patch('imapclient.IMAPClient')
def test_adding_default_text_handler_via_function(mock_IMAP, mock_SMTP):
    """Test adding a default text handler and verify that it replaces the stock handler"""

    client = shawk.Client(username, password)
    client.setup_inbox(password)
    spoof_contact = client.add_contact(number=1234567890, carrier='Verizon', name='Spoof')
    spoof_phone = SpoofPhone(client.imap, spoof_contact)
    context = {}

    def default_text_handler(client, message):
        context['did_call_default_text_handler'] = True

    client.set_default_text_handler(default_text_handler)
    spoof_phone.send('Testing')
    client.refresh()

    assert(context['did_call_default_text_handler'])

@patch('smtplib.SMTP')
@patch('imapclient.IMAPClient')
def test_adding_text_handler_via_function(mock_IMAP, mock_SMTP):
    """Test adding a text handler with regex via function"""

    client = shawk.Client(username, password)
    client.setup_inbox(password)
    spoof_contact = client.add_contact(number=1234567890, carrier='Verizon', name='Spoof')
    spoof_phone = SpoofPhone(client.imap, spoof_contact)
    context = {}

    def text_handler(client, message, match, regex):
        context['did_call_text_handler'] = True

    client.add_text_handler(re.compile('Testing'), text_handler)
    spoof_phone.send('Testing')
    client.refresh()

    assert(context['did_call_text_handler'])

@patch('smtplib.SMTP')
@patch('imapclient.IMAPClient')
def test_adding_text_handler_via_decorator_without_flags(mock_IMAP, mock_SMTP):
    """Test adding a text handler with regex via decorator without flags"""

    client = shawk.Client(username, password)
    client.setup_inbox(password)
    spoof_contact = client.add_contact(number=1234567890, carrier='Verizon', name='Spoof')
    spoof_phone = SpoofPhone(client.imap, spoof_contact)
    context = {}

    @client.text_handler('Testing')
    def text_handler(client, message, match, regex):
        context['did_call_text_handler'] = True

    spoof_phone.send('Testing')
    client.refresh()

    assert(context['did_call_text_handler'])

@patch('smtplib.SMTP')
@patch('imapclient.IMAPClient')
def test_adding_text_handler_via_decorator_with_flags(mock_IMAP, mock_SMTP):
    """Test adding a text handler with regex via decorator with flags"""

    client = shawk.Client(username, password)
    client.setup_inbox(password)
    spoof_contact = client.add_contact(number=1234567890, carrier='Verizon', name='Spoof')
    spoof_phone = SpoofPhone(client.imap, spoof_contact)
    context = {}

    @client.text_handler('testing', 'i')
    def text_handler(client, message, match, regex):
        context['did_call_text_handler'] = True

    spoof_phone.send('Testing')
    client.refresh()

    assert(context['did_call_text_handler'])

@patch('smtplib.SMTP')
@patch('imapclient.IMAPClient')
def test_removing_text_handler(mock_IMAP, mock_SMTP):
    """Test removing a text handler"""

    client = shawk.Client(username, password)
    client.setup_inbox(password)
    spoof_contact = client.add_contact(number=1234567890, carrier='Verizon', name='Spoof')
    spoof_phone = SpoofPhone(client.imap, spoof_contact)
    context = {}

    def text_handler(client, message, match, regex):
        context['did_call_text_handler'] = True

    regex = re.compile('Testing')
    client.add_text_handler(regex, text_handler)
    client.remove_text_handler(regex, text_handler)

    spoof_phone.send('Testing')
    client.refresh()

    assert(not context.get('did_call_text_handler', False))

#
# Test contact handler functions
#

@patch('smtplib.SMTP')
@patch('imapclient.IMAPClient')
def test_adding_contact_handler_via_decorator(mock_IMAP, mock_SMTP):
    """Test adding a contact handler"""

    client = shawk.Client(username, password)
    client.setup_inbox(password)
    spoof_contact = client.add_contact(number=1234567890, carrier='Verizon', name='Spoof')
    spoof_phone = SpoofPhone(client.imap, spoof_contact)
    context = {}

    @client.contact_handler(spoof_contact)
    def decorated_contact_handler(client, message):
        context['did_call_decorated_contact_handler'] = True

    spoof_phone.send('Testing')
    client.refresh()

    assert(context['did_call_decorated_contact_handler'])

@patch('smtplib.SMTP')
@patch('imapclient.IMAPClient')
def test_adding_contact_handler_via_function(mock_IMAP, mock_SMTP):
    """Test adding a contact handler via function"""

    client = shawk.Client(username, password)
    client.setup_inbox(password)
    spoof_contact = client.add_contact(number=1234567890, carrier='Verizon', name='Spoof')
    spoof_phone = SpoofPhone(client.imap, spoof_contact)
    context = {}

    def contact_handler(client, message):
        context['did_call_contact_handler'] = True

    client.add_contact_handler(spoof_contact, contact_handler)
    spoof_phone.send('Testing')
    client.refresh()

    assert(context['did_call_contact_handler'])

@patch('smtplib.SMTP')
@patch('imapclient.IMAPClient')
def test_removing_contact_handler(mock_IMAP, mock_SMTP):
    """Test removing a contact handler"""

    client = shawk.Client(username, password)
    client.setup_inbox(password)
    spoof_contact = client.add_contact(number=1234567890, carrier='Verizon', name='Spoof')
    spoof_phone = SpoofPhone(client.imap, spoof_contact)
    context = {}

    def contact_handler(client, message):
        context['did_call_text_handler'] = True

    client.add_contact_handler(spoof_contact, contact_handler)
    client.remove_text_handler(spoof_contact, contact_handler)

    spoof_phone.send('Testing')
    client.refresh()

    assert(not context.get('did_call_contact_handler', False))

#
# Test emojis
#

@patch('smtplib.SMTP')
def test_sending_emoji_message(mock_SMTP):
    """Test sending a message with emoji"""

    client = shawk.Client(username, password)
    contact = client.add_contact(number=1234567890, carrier='Verizon', name='Somebody')
    smtp_instance = mock_SMTP.return_value
    address = contact.get_address()
    message = 'Testing :thumbs_up_sign:'

    client.send(message, contact=contact)

    assert(smtp_instance.sendmail.call_count == 1)
    assert(smtp_instance.sendmail.mock_calls == [call('0', address, emoji.emojize(message))])

@patch('smtplib.SMTP')
def test_sending_emoji_message_via_send_emojize(mock_SMTP):
    """Test sending a message with emoji by passing emojize=True to send"""

    client = shawk.Client(username, password)
    client.disable_emojize()
    contact = client.add_contact(number=1234567890, carrier='Verizon', name='Somebody')
    smtp_instance = mock_SMTP.return_value
    address = contact.get_address()
    message = 'Testing :thumbs_up_sign:'

    client.send(message, contact=contact, emojize=True)

    assert(smtp_instance.sendmail.call_count == 1)
    assert(smtp_instance.sendmail.mock_calls == [call('0', address, emoji.emojize(message))])

@patch('smtplib.SMTP')
def test_sending_message_without_translating_emoji(mock_SMTP):
    """Test sending a message with emoji code but without emojizing it"""

    client = shawk.Client(username, password)
    client.disable_emojize()
    contact = client.add_contact(number=1234567890, carrier='Verizon', name='Somebody')
    smtp_instance = mock_SMTP.return_value
    address = contact.get_address()
    message = 'Testing :thumbs_up_sign:'

    client.send(message, contact=contact)

    assert(smtp_instance.sendmail.call_count == 1)
    assert(smtp_instance.sendmail.mock_calls == [call('0', address, message)])

@patch('smtplib.SMTP')
@patch('imapclient.IMAPClient')
def test_receiving_emoji_message(mock_IMAP, mock_SMTP):
    """Test receiving a message with emoji"""

    client = shawk.Client(username, password)
    client.disable_demojize()
    client.setup_inbox(password)
    spoof_contact = client.add_contact(number=1234567890, carrier='Verizon', name='Spoof')
    spoof_phone = SpoofPhone(client.imap, spoof_contact)
    message_time = datetime.utcnow()
    original = 'Testing :thumbs_up_sign:'
    emojized = emoji.emojize(original, use_aliases=True)
    spoof_phone.send(original, time=message_time, emojize=True)

    client.refresh()

    assert(client.imap.copy.call_count == 1)
    assert(str(client.inbox) == str([shawk.Message(emojized, spoof_phone.sender, message_time)]))

@patch('smtplib.SMTP')
@patch('imapclient.IMAPClient')
def test_receiving_emoji_message_demojized(mock_IMAP, mock_SMTP):
    """Test receiving a message with emoji translated back to text"""

    client = shawk.Client(username, password)
    client.setup_inbox(password)
    spoof_contact = client.add_contact(number=1234567890, carrier='Verizon', name='Spoof')
    spoof_phone = SpoofPhone(client.imap, spoof_contact)
    message_time = datetime.utcnow()
    original = 'Testing :thumbs_up_sign:'
    emojized = emoji.emojize(original, use_aliases=True)
    spoof_phone.send(original, time=message_time, emojize=True)

    client.refresh()

    assert(client.imap.copy.call_count == 1)
    assert(str(client.inbox) == str([shawk.Message(original, spoof_phone.sender, message_time)]))
