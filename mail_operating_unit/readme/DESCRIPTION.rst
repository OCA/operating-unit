This module introduces the following features:

- It introduces the operating unit (OU) to mail.
- We have the possibility to set an outgoing mail for each OU.
- We have the possibility to set the OU for each mail alias.
- We have the possibility to set the OU on each user for mails if operating_unit_id does not exist on record.
- If an OU is set in an mail alias it sets the domain according its OU.
- We have the possibility to set the OU for each mail template.
- If we sent a mail (ex. via sale order) we can only select the templates of
  the same model where the OU is not set or of the same OU.
- If we sent a mail within a record it sets the sender_email_address (alias and
  domain) and reply_to according its OU.
