.. image:: https://img.shields.io/badge/license-LGPLv3-blue.svg
   :target: https://www.gnu.org/licenses/lgpl.html
   :alt: License: LGPL-3

===============================
Accounting with Operating Units
===============================

This module allows a company to manage the accounting based on Operating
Units (OU's).

* The financial reports (Trial Balance, P&L, Balance Sheet), allow to report
  the balances of one or more OU's.

* If a company wishes to report Balance Sheet and P&L accounts based on
  OU's, they should indicate at company level that the OU's are
  self-balanced, and the corresponding Inter-Operating Unit clearing account.
  The Chart of Accounts will always be balanced, for each Operating Unit.

* A company considering Operating Unit as applicable to report only profits
  and losses will not need to set the OU's as self-balanced.

* The self-balancing of Operating Unit is ensured at the time of posting a
  journal entry. In case that the journal involves posting of items in
  separate Operating Units, new journal items will be created, using the
  Inter-Operating Unit clearing account, to ensure that each OU is going to
  be self-balanced for that journal entry.

* Adds the Operating Unit (OU) to the invoice. A user can choose what OU to
  create the invoice for.

* Adds the Operating Unit (OU) to payments and payment methods. The operating
  unit of a payment will be that of the payment method chosen.

* Implements security rules at OU level to invoices, payments and journal
  items.


Installation
============

No specific installation requirements.

Configuration
=============

If your company is required to generate a balanced balance sheet by
Operating Unit you can specify at company level that Operating Units should
be self-balanced, and then indicate a self-balancing clearing account.

1. Create an account "Inter-OU Clearing". It is a balance sheet account.

2. Go to *Settings / Companies / Configuration* and Set the "Operating Units
   are self-balanced" checkbox.

   Then set the "Inter-OU Clearing"  account in "Inter-Operating Unit
   clearing account" field.

3. Go to *Accounting / Configuration / Accounting / Journals* and define, for
   each Payment Method (journals of type cash or bank), the Operating Unit
   that will be used in payments.


Usage
=====

* Add the Operating Unit to invoices.

* Report invoices by Operating Unit in *Accounting / Reporting*
  *Business Intelligence / Invoices*

* Add the Default Operating Unit to account move. Then all move lines will
  by default adopt this Operating Unit.

* Add Operating Units to the move lines.

  If they differ across lines of the same move, and the OU's are
  self-balanced, then additional move lines will be created so as to make
  the move self-balanced from OU perspective.

* In the menu *Accounting / Reporting / PDF Reports*, you can indicate the
  Operating Units to report on, for the *Trial Balance*, *Balance Sheet*,
  *Profit and Loss*, and *Financial Reports*.


.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/213/10.0

Known issues / Roadmap
======================

* The *General Ledger*, *Aged Partner Balance* reports do not support the
  filter by Operating Unit. Basically due to lack of proper hooks in the
  standard methods used by these reports, to introduce the ability to filter
  by Operating Unit.


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/operating-unit/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Eficent Business and IT Consulting Services S.L. <contact@eficent.com>
* Jordi Ballester Alomar <jordi.ballester@eficent.com>
* Aarón Henríquez <ahenriquez@eficent.com>
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
