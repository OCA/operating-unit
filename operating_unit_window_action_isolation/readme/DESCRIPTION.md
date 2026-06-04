This module extends Odoo window actions to automatically restrict
records according to the user's default operating unit.

When a user opens a menu linked to an `ir.actions.act_window`, an
additional domain is injected when:

- The user is not the superuser.
- The user has a default operating unit configured.
- The target model contains an `operating_unit_id` field.

The injected domain allows access to:

- Records belonging to the user's default operating unit.
- Records without an operating unit assigned.