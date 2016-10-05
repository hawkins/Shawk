# <img src="https://raw.githubusercontent.com/hawkins/shawk/master/shawk.png" width="64" height="64"</img> Shawk - Free SMS with Python using SMTP and IMAP

A python `smtplib` and `imapclient` wrapper to send and receive SMS messages through SMS gateways with a Gmail login. Perfect for Internet of Things projects that use a Raspberry Pi to text you!


##### Disclaimer

> This project is a work in progress, and as such, the API may change drastically before version 1.0 is reached. This repo may be out-of-sync with the PyPi version, so if you're interested in using the bleeding-edge features added since last tag, clone the repo and import locally. Tags will reflect PyPi published versions.


# Installation

Shawk is available on PyPi as such:

```
pip install shawk
```

# Documentation

To see full documentation and a more detailed Getting Started page, [see here](https://shawk.readthedocs.io/en/latest/Getting%20Started.html).


# Simple Usage Example

## Sending Messages

#### Create a Client:

Simply `import shawk` and define a Client by providing a Gmail username and password.

```Python
import shawk
client = shawk.Client('username@gmail.com', 'password')
```


#### (Optionally) Add Contacts:

Use the `add_contact()` function to add a contact's number as string or integer, carrier, and (optionally) a name. You can even pass in a lists of multiple numbers, names, and carriers.

```Python
client.add_contact("5551234567", 'Carrier', 'Name')
client.add_contact("18008675309", 'Carrier')
```


#### Send SMS:

Shawk can send texts either by providing a Contact object, phone number, or name.

```Python
client.send("Message content to send", SomeContact) # or contact=SomeContact
client.send("Message content to send", name="Name")
client.send("Message content to send", number="5551234567")
```


## Receiving Messages Automatically

Shawk clients can be configured to automatically refresh their inbox and report back with new messages.
In this mode, Shawk will poll the IMAP server periodically and check for new messages.

To do this, create your client with the `auto=True` parameter, or [see the docs](https://shawk.readthedocs.io/en/latest/Client.html#shawk.Client.Client.setup_inbox) for other methods.

```Python
client = Shawk.Client('username@gmail.com', 'password', auto=True)
```

You can also change how frequently the server is queried:

```Python
client.set_refresh_interval(30) # Period time in seconds
```

Each time Shawk encounters a new message, it will pass its Message object to the handler function.
You can define the behavior here with `client.set_handler(some_function)` where `some_function` accepts a Message object.

For example:

```Python
@client.text_handler()
def handler(client, msg):
    print("Hey, we're popular! {} texted us!".format(msg.sender))
    if isinstance(msg.sender, str):                      # if msg.sender is a string
        client.send("Hello, world!", address=msg.sender) # then msg.sender is an address
    else:
        client.send("Hello, world!", msg.sender)         # then msg.sender is a Contact
```
