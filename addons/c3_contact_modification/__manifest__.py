{
    "name": "C3 Contact Modification",
    "summary": "Extends Odoo Contacts with C3 contact setup customizations.",
    "version": "19.0.1.10.0",
    "category": "Contacts",
    "author": "Wadprog",
    "license": "LGPL-3",
    "depends": ["contacts"],
    "data": [
        "data/contact_tags.xml",
        "views/res_partner_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
