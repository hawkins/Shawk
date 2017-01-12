Using Emoji
===========

Syntax
------

Using Emoji in Shawk is pretty straightforward.
Since Shawk utilizies the Emoji library on PyPi, the entire set of Emoji codes as defined by the `unicode consortium <http://www.unicode.org/Public/emoji/1.0/full-emoji-list.html>`_ is supported in addition to a bunch of `aliases <http://www.emoji-cheat-sheet.com/>`_.

Unlike the Emoji library, we allow all aliases at all times.
This means that you can say either ":thumbs_up_sign:" or ":thumbsup:" to insert the thumbs up emoji in your text messages.


Configuring
-----------

By default, both "demojizing" and "emojizing" are enabled.
This means that when you receive a text message, it is "demojized", or emojis are translated to :: syntax, and sent messages are translated from :: syntax to unicode emojis.

To disable emojizing / demojizing, you can run the following code:

.. code-block:: python

    # Disable demojizing
    client.disable_demojize()

    # Disable emojizing
    client.disable_emojize()

You can similarly re-enable either setting:

.. code-block:: python

    # Re-enable demojizing
    client.enable_demojize()

    # Re-enable emojizing
    client.enable_emojize()


Example
-------

Since emojizing is enabled by default, sending an emojized message is as simple as this:

.. code-block:: python

    # Create and configure client
    client = shawk.Client(username, password)
    contact = client.add_contact(number=1234567890, carrier='Verizon', name='Somebody')

    # Send the message
    client.send('Testing :thumbs_up_sign:', contact=contact)
