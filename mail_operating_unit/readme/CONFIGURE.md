To configure this module, you need to:

- Assign an *Alias Domain* to each Operating Unit that should use a specific email domain.
- Assign an *Operating Unit* to an Email Template when emails sent from that template must use the alias domain of that operating unit.
- Optionally assign an *Outgoing Mail Server* to an Operating Unit when emails should be routed through a specific SMTP server.

When no operating unit is defined on the template or on the target record, the standard Odoo alias domain behavior is applied.

When no unambiguous Operating Unit mail server can be determined, the standard Odoo outgoing mail server selection is applied.
