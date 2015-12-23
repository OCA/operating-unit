.. image:: https://img.shields.io/badge/license-LGPLv3-blue.svg
   :target: https://www.gnu.org/licenses/lgpl.html
   :alt: License: LGPL-3

==========================
Stock with Operating Units
==========================

This module introduces the following features:
- Adds the operating unit to the Warehouse.
- Adds the operating unit to the Stock Location.
- Adds the requesting operating unit to stock pickings.
- Implements user's security access rules.

Installation
============

No external library is used.

Configuration
=============

To configure this module, you need to:

* Assign Operating Unit to Warehouses.
* Assign Operating Unit to Stock Locations.

Usage
=====

This module defines the operating unit entity and the user's security rules.
Other modules extend the standard Odoo apps with the OU.

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
operating_unit%0Aversion:%20
9.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Eficent <contact@eficent.com>
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