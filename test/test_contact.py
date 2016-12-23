
# Import shawk
import shawk

# Prepare contacts used throughout tests
mini_contact = shawk.Contact(12345678, 'Verizon')
name_contact = shawk.Contact(12345678, 'Verizon', 'Somebody')


""" BEGIN TESTS """


def test_repr_minimal():
    assert(repr(mini_contact) == "<shawk.Contact('12345678', 'Verizon', '<No name>')>") 

def test_repr_with_name():
    assert(repr(name_contact) == "<shawk.Contact('12345678', 'Verizon', 'Somebody')>")

def test_string_minimal():
    assert(str(mini_contact) == '<No name>: 12345678 (Verizon)')

def test_string_with_name():
    assert(str(name_contact) == 'Somebody: 12345678 (Verizon)')

def test_get_address_verizon():
    assert(name_contact.get_address() == '12345678@vtext.com')

# TODO: Ideally we would test every domain, right?

def test_get_number():
    assert(name_contact.get_number() == '12345678')

def test_get_name():
    assert(name_contact.get_name() == 'Somebody')

