Getting Started
===============

.. _getting-started:
.. highlight:: python

The idea of Shawk is to provide an easy-to-use interface for sending and receiving text messages.
This getting started guide will give you a quick run-down on the highlights of how to use Shawk.

.. toctree::
   :hidden:
   :caption: Table of Contents
   :maxdepth: 2


Installing Shawk
----------------

Installing Shawk is easy.
Simply run `pip install shawk` to download and install the latest version.

To best understand how to use shawk, let's break it down into a few features:

- Creating a client
- Adding/removing contacts
- Sending messages
- Manually retrieving messages
- Automatically retrieving messages
- Defining behavior for new messages


Creating a client
-----------------

The first thing you'll want to do after installing Shawk is create a client.
This is the main interface you'll use in Shawk.
You can define multiple clients, of course, but for the sake of this tutorial, we'll just use one.

If we say our Gmail login username is `"username@gmail.com"` and our password is `"password"`, then we can create our client like this:

.. code-block:: python

    import shawk

    user = "username@gmail.com"
    password = "password"
    client = shawk.Client(user, password)


Adding/removing contacts
------------------------

Adding contacts will be helpful for understanding who texted your client or specifying who you would like to text in an easy and readable manner.
Email gateways are a bit wonky at best, so contacts require both a phone number and carrier.
Additionally, you can specify a contact name to make things easier, but that is optional.

Say you want to add a contact Josh who uses Verizon and has a phone number of 1234567890.

You can add them as such:

.. code-block:: python

    client.add_contact(1234567890, 'Verizon', 'Josh') # Note: name/'Josh' is optional

You can similarly remove them in any of the following ways:

.. code-block:: python

    client.remove_contact(contact) # Where contact is some shawk.Contact object, which you can get from messages
    # or
    client.remove_contact(number=1234567890)
    # or
    client.remove_contact(name='Josh')


Sending messages
----------------

You're limited to texting only your contacts you've previously defined, or those whose explicit address you have obtained.
This is, in-part, a restriction to prevent spam bots from abusing Shawk, but also a means of simplifying Number to Address mappings.
What this means is, in order to send someone a text message, you can either add them as a contact or reply to a message they send you.

So, if you defined a contact, you can text them by specifying their name, number, or Contact:

.. code-block:: python

    client.send('Hey, Josh!', name='Josh')
    # or
    client.send('Hey, Josh!', number=1234567890)
    # or
    client.send('Hey, Josh!', contact)


Manually retrieving messages
----------------------------

There are two ways to get new messages in Shawk: Manually or Automatically.

We can get the new ones manually by first setting up our inbox and refreshing it:

.. code-block:: python

    client.setup_inbox(password) # We don't save your password, so send it again
    client.refresh_inbox()

    # or...
    client.setup_inbox(password, refresh=True)

This will handle the IMAP server connection for retrieving new messages to your Gmail account.

You can actually use a distinct Gmail account from the one you use to send messages by passing a user: string, but we won't focus on that for this simple tutorial.
As always, read the rest of the docs if you'd like to know more about that.


Automatically retrieving messages
---------------------------------

You can configure Shawk to automatically retrieve new messages for you pretty easily.
This will cause the client to refresh its inbox periodically on time interval (found in client.refresh_interval).

To do this, setup your inbox as such:

.. code-block:: python

    client.setup_inbox(password)
    client.enable_auto_refresh()

    # or...
    client.setup_inbox(password, auto=True)


Boom. Done. Your client now automatically pings the server and looks for new messages!

You can configure the time interval with `client.set_interval()`, which you can read more about in the docs.


Defining behavior for new messages
----------------------------------

At this point, I hope you've asked yourself, "But what will Shawk do when it receives a message?"
By default, Shawk will simply print the contents of the new messages when it finds them.

That's not particularly useful, so we'll let you dictate how Shawk `should` be used.

This default behavior can be overridden by defining one or more handler functions that receive a client, message, and a regex match object.
These handler function are just callback functions with the `@client.text_handler(regex)` decorator, where regex is some regular expression in string form.

If no regex is provided, then the function is considered the default case handler, and will be used whenever no other handler's regex pattern match a received text.

Whew.


So, you can define your own behavior as follows:

.. code-block:: python

    c = shawk.Client('username@gmail.com', 'password')
    c.setup_inbox('password')

    @client.text_handler() # No arguments, so Shawk knows this is our default handler
    def handler(client, msg):
        print("Hey, we're popular! %s texted us!" % msg.sender)
        print("Received: %s" % msg.text)

        client.send("I am replying to your text!", msg.sender)

    # Or with a regex
    @client.text_handler('^Print (.*)', 'i') # Starts with "print" (case insensitive because of 'i' flag), matches text following.
    def print_dot_z(client, msg, match, regex):
        print(match.group(1))

Naturally, you'll do something a bit more meaningful in your handler functions.
But since they're just simple python functions, you've got free reign to interface with your scripts however you like.

Note that you can also create handlers that activate on Contacts instead of Regex.
This is useful if you only want behavior to apply to a specific contact and consider text second, instead of the other way around.

You can do this like so:

.. code-block:: python

    josh_contact = client.add_contact(1234567890, 'Verizon', Josh)

    @client.contact_handler(josh_contact)
    def josh_handler(client, msg):
        print("This func only called if Josh texted us")

Also worth mentioning is that these are just normal functions, so you can define handlers that hook onto contacts within other handlers.
I.e., a text_handler that when called will instantiate a contact_handler to continue the conversation with that specific contact after they reply.
This is advanced behavior tho - so we we'll cover that in another guide.

I hope you've found that Shawk is pretty easy to use, yet very powerful, since it allows your users to provide input and receive output via SMS, for free.

If you encounter any issues or have any questions, you can post them on `GitHub://hawkins/shawk <https://github.com/hawkins/shawk>`_.
