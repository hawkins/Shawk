
# Import shawk
from shawk import Message, Contact

# Prepare contacts used throughout tests
name_contact = Contact(12345678, 'Verizon', 'Somebody')

# Prepare messages
mini_message = Message('Text', name_contact)
date_message = Message('Text', name_contact, '2016-12-22 21:54:57')
date_message_clone = Message('Text', name_contact, '2016-12-22 21:54:57')

def test_repr_minimal():
    assert(repr(mini_message) == "<shawk.Message('Text', 'Somebody: 12345678 (Verizon)')>")

def test_repr_with_date():
    assert(repr(date_message) == "<shawk.Message('Text', 'Somebody: 12345678 (Verizon)', '2016-12-22 21:54:57')>")

def test_string_minimal():
    assert(str(mini_message) == "Message from Somebody: 12345678 (Verizon) at None: \"Text\"")

def test_string_with_date():
    assert(str(date_message) == "Message from Somebody: 12345678 (Verizon) at 2016-12-22 21:54:57: \"Text\"")

def test_not_eq():
    assert(not (mini_message == date_message))

def test_eq():
    assert(date_message == date_message_clone)
