.. image:: https://img.shields.io/badge/license-LGPLv3-blue.svg
   :target: https://www.gnu.org/licenses/lgpl.html
   :alt: License: LGPL-3

==============================
Account Voucher Operating Unit
==============================

This module introduces Operating Units to the Account Voucher model. It also
introduces security rules to manage access control only to users that can
operate on the OU of the voucher.

Customer or Supplier Receipts
-----------------------------

* The Operating Unit is assigned to the voucher, and then to the journal
  items when the voucher is posted.


Configuration
=============

To configure this module, you need to:

* For each bank/cash GL account that you intend to use in customer or supplier
  payments you have to define the default Operating Unit that the payment
  will be posted to. Go to *Invoicing / Configuration / Accounts / Accounts*
  and search for your bank/cash accounts. Then add the default Operating Unit.


Installation
============

You will need to install also the module 'Account Voucher Move Line Create
Hooks' that is available in the `OCA/account-payment <https://github
.com/OCA/operating_unit/issues>`_ repository.


Usage
=====

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/213/9.0

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


To contribute to this module, please visit http://odoo-community.org.
