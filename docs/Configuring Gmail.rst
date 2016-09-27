Configuring Gmail
=================

SMTP
----

GMail should work with SMTP out of the box, but currently sending messages is limited to **roughly 100 messages per 24 hours**.
After your limit is reached, the limit will be reset 24 hours later.

However, you can greatly increase these limits (**10,000 messages per 24 hours** by creating a Google Apps account.
You can find out more about this `here <https://support.google.com/a/answer/2956491#sendinglimitsforrelay>`_.


IMAP
----

1. Create a Google / Gmail account for your application (It doesn't have to be new, but I suggest you do not use your personal / work account).

2. Follow instructions to `set up an App password here <https://support.google.com/accounts/answer/185833?hl=en>`_ and be sure to select app "Other (custom name)" and enter anything to help you remember it. I.e., "shawk".

    **Be careful though, as this password grants full access to your Google account! Do not share this with anyone and do not commit it!**

    I recommend creating a `secure.ini` file which your scripts will read in your password from. Add this file to your `.gitignore` to prevent accidentally commiting it.

3. Follow instructions to `enable IMAP access to Gmail here <https://support.google.com/mail/answer/7126229?hl=en>`_. You only need to complete Step 1, don't worry about Step 2. The Shawk library handles Step 2 for you.

