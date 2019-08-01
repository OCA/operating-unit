#. Create an Outgoing Mail Server.
#. Use a current Operating Unit (OU) or create a new one.
#. Set values into the new fields 'Catchall alias', 'Catchall domain',
   'Outgoing Mail Server').
#. Assignment of an OU to a mail alias. Then it takes the domain set in the OU
   as domain for this mail alias. If no OU set, it takes the one from system
   parameters. If the set OU has no 'Catchall domain' set, it stays
   empty.
#. Assignment of an OU to a mail template. If we sent a mail (ex. via sale
   order) we can only select the templates of the same model where the OU is
   not set or of the same OU. If we sent a mail within a record it sets the
   sender_email_address (alias and domain) and reply_to according its OU.
