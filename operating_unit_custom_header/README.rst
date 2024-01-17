=====================================================
Operating Unit Custom Header
=====================================================

This module adds custom header and footer by operating unit on reports
The header and footer of the Operating Unit will appears on the report
instead of the company header and footer.
This module works with the four Odoo layout: light, boxed, clean and
background.


Configuration
=============

* Go to Settings / Users & Companies / Operating Units and modify the header and footer. By default, they are a copy of the company header and footer.


    note::
    Ex. to change the logo in the header:

    *<img t-if="o.operating_unit_id.partner_id.image_1920" t-att-src="image_data_uri(o.operating_unit_id.partner_id.image_1920)" style="max-height: 45px;" alt="Logo"/>*


Bug Tracker
===========

Problems with the module?
Write to: <support@archeti.com>


Credits
=======

Authors
~~~~~~~

* ArcheTI

Contributors
------------


* Cécile Jallais <cjallais@archeti.com>


.. image:: https://www.archeti.com/logo.png
   :alt: ArcheTI
   :target: https://archeti.com
