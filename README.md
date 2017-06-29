# <img alt="Shawk Logo" src="https://raw.githubusercontent.com/hawkins/shawk/master/shawk.png" width="64" height="64"/> Shawk - Free SMS with Python using SMTP and IMAP

A Python `smtplib` and `imapclient` wrapper to send and receive SMS messages through SMS gateways with a Gmail login.
Perfect for Internet of Things projects that use a Raspberry Pi to text you.


##### Disclaimer

> This project is a work in progress, and as such, the API may change drastically before version 1.0 is reached. This repo may be out-of-sync with the PyPi version, so if you're interested in using the bleeding-edge features added since last tag, clone the repo and import locally. Tags will reflect PyPi published versions.


# Installation

Shawk is available on PyPi as such:

```
pip install -U shawk
```


# Documentation

To see full documentation and a more detailed Getting Started page, [see here](https://shawk.readthedocs.io/en/latest/Getting%20Started.html).


# Contributing

I welcome all sorts of contributions - code, docs, tests, bugs, etc.
If you'd like to contribute code, please make sure your tests continue to pass after making your changes.
Additionally, if your new code requires any testing, please write your tests in the appropriate file.


## Testing

Tests can be run with Pytest.

1. Run `pip install -U pytest` to install pytest
2. Locally install this Shawk package with `pip install -e .`
3. Then simply run `pytest` in the root directory to execute tests


# Simple Usage Example

## Sending Messages

#### Create a Client:

Simply `import shawk` and define a Client by providing a Gmail username and password.

```Python
import shawk
client = shawk.Client('username@gmail.com', 'password')
```


#### (Optionally) Add Contacts:

Use the `add_contact()` function to add a contact's number as string or integer, carrier, and (optionally) a name.

```Python
some_contact = client.add_contact("5551234567", 'Carrier', 'Name')
```


#### Send SMS:

Shawk can send texts either by providing a Contact object, phone number, or name.

```Python
client.send("Message content to send", some_contact) # or contact=some_contact
client.send("Message content to send", name="Name")
client.send("Message content to send", number="5551234567")
```


## Receiving Messages Automatically

Shawk clients can be configured to automatically refresh their inbox and report back with new messages.
In this mode, Shawk will poll the IMAP server periodically and check for new messages.

To do this, create your client with the `auto=True` parameter, or [see the docs](https://shawk.readthedocs.io/en/latest/Client.html#shawk.Client.Client.setup_inbox) for other methods.

```Python
client = Shawk.Client('username@gmail.com', 'password')
client.setup_inbox('password', auto=True)
```

You can also change how frequently the server is queried:

```Python
client.set_refresh_interval(30) # Period time in seconds
```

Each time Shawk encounters a new message, it will pass its Message object to the handler function.
You can define new behaviors by creating functions with the `@client.text_handler(regex, flags)` or `@client.contact_handler(contact)` decorators.

This allows you to define certain behaviors based on who texted you or what was in the message without complicating your actual behavior logic.

For a small example:

```Python
@client.text_handler()
def handler(client, msg):
    print("Hey, we're popular! {} texted us!".format(msg.sender))
    client.send("Hello, world!", msg.sender)
```

You can define more complicated text_handlers and contact_handlers, but we'll save that for the docs.
