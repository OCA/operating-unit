.. image:: https://img.shields.io/badge/license-LGPLv3-blue.svg
   :target: https://www.gnu.org/licenses/lgpl.html
   :alt: License: LGPL-3

=======================================
Stock account moves with Operating Unit
=======================================

This module introduces the following features:

- Creates account move lines when stock moves are posted between internal
  locations within the same company, but different OU’s.


Configuration
=============

If your company is required to generate a balanced balance sheet by
operating unit you can specify at company level that operating units should
be self-balanced, and then indicate a self-balancing clearing account.

#. Create an account for "Inter-OU Clearing" of type Regular.
#. Go to *Settings / Companies / Configuration* and:

   * Set the "Operating Units are self-balanced" checkbox.

   * Set the "Inter-OU Clearing"  account in "Inter-operating unit clearing
     account" field.

#. Assign Operating Unit in Accounts.


Usage
=====

Create stock moves between internal locations within the same company, but
different OU’s. The journal entries are created and they are self-balanced
within the OU when the journal entries are posted

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/213/10.0

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
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
