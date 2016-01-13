.. image:: https://img.shields.io/badge/license-LGPLv3-blue.svg
   :target: https://www.gnu.org/licenses/lgpl.html
   :alt: License: LGPL-3

===============================
Accounting with Operating Units
===============================

This module introduces the following features:
- Adds the Operating Unit in the account move line.
- Defines if the operating units are self-balanced and Inter-operating unit
clearing account at company level.
- When users create a journal entry with lines in different operating units,
if operating units have been defined to be self-balanced,
at the time of posting the journal entry it automatically creates the
corresponding lines in the Inter-operating unit clearing account,
making each OU self-balanced.
- The account financial reports include the option to filter by OU.
- Adds the Operating Unit in the invoice
- Implements security rules in the invoice

Installation
============

No external library is used.

Configuration
=============

If your company is required to generate a balanced balance sheet by
operating unit you can specify at company level that operating units should
be self-balanced, and then indicate a self-balancing clearing account.

* Create an account for "Inter-OU Clearing" of type Regular.
* Go to *Settings / Companies / Companies* and:
** Set the "Operating Units are self-balanced" checkbox
** Set the "Inter-OU Clearing"  account in "Inter-operating unit clearing
account" field.

* Assign Operating Unit in Accounts.


Usage
=====

Every accounting entry must balance both at the total level and at the level
of the operating units defined in the journal entry.
If the accounting entry does not balance at the level of the operating units,
additional account entries are created automatically to balance the accounting
entry.


.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/213/9.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/213/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed `feedback
<https://github.com/OCA/
213/issues/new?body=module:%20
account_operating_unit%0Aversion:%20
9.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Eficent Business and IT Consulting Services S.L. <contact@eficent.com>
* Serpent Consulting Services Pvt. Ltd. <support@serpentcs.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.