.. image:: https://img.shields.io/badge/license-LGPLv3-blue.svg
   :target: https://www.gnu.org/licenses/lgpl.html
   :alt: License: LGPL-3

===============================
Accounting with Operating Units
===============================

This module introduces the following features:

* Adds the Operating Unit (OU) to the account move line.

* Defines if the Operating Units are self-balanced and Inter-Operating Unit
  clearing account at company level.

* Journal entry with lines in different Operating Units are checked based on
  the "self-balanced" set up in OU.

  At the time of posting the journal entry, the corresponding lines in the
  Inter-Operating Unit clearing account are automatically created, making
  each OU self-balanced.

* The account financial reports include the option to filter by OU.

* Adds the Operating Unit (OU) to the invoice.

* Implements security rules in the invoice based on OU.

Installation
============

No specific installation requirements.

Configuration
=============

If your company is required to generate a balanced balance sheet by
Operating Unit you can specify at company level that Operating Units should
be self-balanced, and then indicate a self-balancing clearing account.

* Create an account for "Inter-OU Clearing" of type Regular.

* Go to *Settings / Companies / Companies* and Set the "Operating Units are
  self-balanced" checkbox.

  Then Set the "Inter-OU Clearing"  account in "Inter-Operating Unit
  clearing account" field.

* Assign Operating Unit in Accounts.


Usage
=====

* Add the Operating Unit to invoices.

* Add the Default Operating Unit to account move. Then all move lines will
  by default adopt this Operating Unit.

* Add Operating Units to the move lines.

  If they differ across lines of the same move, and the OU's are
  self-balanced, then additional move lines will be created so as to make
  the move self-balanced from OU perspective.

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
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.