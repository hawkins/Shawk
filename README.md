# <img src="https://raw.githubusercontent.com/hawkins/shawk/master/shawk.png" width="64" height="64"</img> Shawk - Free SMS with Python using SMTP and IMAP

A python `smtplib` and `imapclient` wrapper to send and receive SMS messages through SMS gateways with a Gmail login. Perfect for Internet of Things projects that use a Raspberry Pi to text you!


##### Disclaimer

> This project is a work in progress, and as such API may change drastically before version 1.0 is reached. This repo may be out-of-sync with the PyPi version, so if you're interested in using the bleeding-edge features added since last tag, clone the repo and import locally. Tags will reflect PyPi published versions.


# Installation

Shawk is available on PyPi as such:

```
pip install shawk
```


# Usage

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

#### Lookup Contacts

You can lookup contacts by address, which is equivalent to `contact.get_address()`, or by providing a message in which the contact is the sender.

```Python
for message in client.inbox:
    contact = client.get_contact_from_address('5551234567@Carrier.address') # By address
    contact = client.get_contact(message) # By message sender
```


#### Send SMS:

Shawk can send texts either by providing a Contact object, phone number, or name.

```Python
client.send("Message content to send", SomeContact) # or contact=SomeContact
client.send("Message content to send", name="Name")
client.send("Message content to send", number="5551234567")
```


## Receiving Messages

### Automatically

Shawk clients can be configured to automatically refresh their inbox and report back with new messages.
In this mode, Shawk will poll the IMAP server periodically and check for new messages.

To do this, create your client with the `auto=True` parameter, or call `client.enable_auto_refresh()` and `client.refresh_automatically()`.
For example:

```Python
client = Shawk.Client('username@gmail.com', 'password', auto=True)
# Or
client.enable_auto_refresh()
client.refresh_automatically()
# Similarly, you can disable/stop auto refreshing with
client.disable_auto_refresh()
```

You can also change how frequently the server is queried:

```Python
client.set_refresh_interval(30) # Period time in seconds
```

Each time Shawk encounters a new message, it will pass its Message object to the handler function.
By default, this simply prints out the Message as a string.
You can override this with `client.set_handler(some_function)` where `some_function` accepts a Message object.

For example:

```Python
def handler(client, msg):
    print("Hey, we're popular! {} texted us!".format(msg.sender))
    client.send("Hello, world!", msg.sender)         # if msg.sender is a contact
    client.send("Hello, world!", address=msg.sender) # if msg.sender is an address

client.set_handler(handler)
```


### Manually

Messages can be loaded by calling `client.refresh_inbox()` which will update `client.inbox` as well as return any new messages.
You'll likely want to loop through these messages and spot new ones to respond to.

```Python
client.refresh_inbox()

for message in client.inbox:
    content = message.text
```


#### Respond to Message

You can get contacts from a message in order to more easily respond.

```Python
for message in client.inbox:
    contact = client.get_contact(message)
    client.send("Message received", contact)
```
