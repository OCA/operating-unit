This module allows companies working with multiple Operating Units to send emails with the appropriate email domain and, optionally, the appropriate outgoing mail server depending on the Operating Unit context.

It lets you define an Alias Domain on an Operating Unit and use that domain automatically when emails are generated from templates or records linked to that Operating Unit.

It also allows you to define an Outgoing Mail Server on an Operating Unit and automatically route emails through that server when no mail server is explicitly defined on the email template.

This is especially useful in multi-brand or multi-entity environments where each Operating Unit must send emails using its own domain and SMTP server, while still keeping the standard Odoo behavior as a fallback when no specific Operating Unit configuration can be determined.
