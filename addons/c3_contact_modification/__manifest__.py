{
    "name": "C3 Contact Modification",
    "summary": "Extends Odoo Contacts with C3 contact setup customizations.",

    "description": """
    This module extends Odoo Contacts with C3 contact setup customizations.
    It adds a required Gender field for individual contacts, and protected contact tags for individuals and companies.
    It also adds an ID Document field for individual contacts.
    It does not add a new app, menu, or separate custom view flow. Users should keep working inside the standard Odoo Contacts app.

    This module is part of the C3 Edition project.
    Module page: https://wadprog.github.io/odoo-c3-contact-modification/
    """,
    "version": "19.0.1.12.0",
    "category": "Contacts",
    "author": "Wadprog",
    "license": "LGPL-3",
    "depends": ["contacts"],
    "data": [
        "data/contact_tags.xml",
        "views/res_partner_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "c3_contact_modification/static/src/fields/c3_id_document_binary_field.js",
            "c3_contact_modification/static/src/fields/c3_id_document_binary_field.xml",
        ],
        "web.assets_unit_tests": [
            "c3_contact_modification/static/tests/fields/c3_id_document_binary_field.test.js",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}
