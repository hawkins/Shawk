Shawk - Free SMS with Python using SMTP
----

A python `smtplib` wrapper to send SMS messages through SMS gateways with a Gmail login.

# Instalation
Shawk is available on PyPi as such:
```
pip install shawk
```

# Usage
## Creation of Client:
Simply import shawk and define a Client by providing a Gmail username and password.
```
import shawk
client = shawk.Client('username@gmail.com', 'password')
```

## Optionally add Contacts:
Use the addContact function to add a contact's number as string or integer, carrier, and optionally a name.
```
client.addContact("5551234567", 'Carrier', 'Name')
```

## Send SMS:
Shawk can send texts either by providing a phone number or name.
```
client.send("Message content to send", name="Name")
client.send("Message content to send", number="5551234567")
```
