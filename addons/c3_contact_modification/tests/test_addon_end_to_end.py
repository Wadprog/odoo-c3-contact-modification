"""End-to-end verification for the C3 contact modification addon."""

from datetime import date, timedelta

from lxml import etree

from odoo import Command
from odoo.exceptions import UserError, ValidationError
from odoo.tests import TransactionCase, tagged

from odoo.addons.c3_contact_modification.models.res_partner_category import (
    C3_CONTACT_TAGS,
    MODULE,
)


@tagged("post_install", "-at_install")
class TestAddonEndToEnd(TransactionCase):
    def test_installed_addon_contact_workflow(self):
        partners = self.env["res.partner"]
        protected_tag = self.env.ref(f"{MODULE}.{C3_CONTACT_TAGS[0][0]}")

        person = partners.create(
            {
                "name": "Doe Alice",
                "is_company": False,
                "type": "contact",
                "gender": "female",
                "date_of_birth": date(1990, 1, 2),
                "category_id": [Command.link(protected_tag.id)],
            }
        )
        company = partners.create(
            {
                "name": "C3 End-to-End Company",
                "is_company": True,
                "type": "contact",
                "category_id": [Command.link(protected_tag.id)],
            }
        )

        self.assertEqual(person.gender, "female")
        self.assertEqual(person.date_of_birth, date(1990, 1, 2))
        self.assertIn(protected_tag, person.category_id)
        self.assertFalse(company.gender)
        self.assertFalse(company.date_of_birth)
        self.assertIn(protected_tag, company.category_id)

        with self.assertRaisesRegex(
            ValidationError,
            "Gender is required for individual contacts.",
        ):
            partners.create(
                {
                    "name": "Missing Gender",
                    "is_company": False,
                    "type": "contact",
                }
            )

        with self.assertRaisesRegex(
            ValidationError,
            "Date of birth is required for individual contacts.",
        ):
            partners.create(
                {
                    "name": "Missing DOB",
                    "is_company": False,
                    "type": "contact",
                    "gender": "female",
                }
            )

        with self.assertRaisesRegex(
            ValidationError,
            "Date of birth cannot be in the future.",
        ):
            partners.create(
                {
                    "name": "Future DOB",
                    "is_company": False,
                    "type": "contact",
                    "gender": "female",
                    "date_of_birth": date.today() + timedelta(days=1),
                }
            )

        with self.assertRaisesRegex(
            UserError,
            "This contact tag is protected by the contact setup module.",
        ):
            protected_tag.sudo().write({"name": "Changed"})

    def test_installed_addon_form_view_contract(self):
        view = self.env["res.partner"].get_view(
            view_id=self.env.ref("base.view_partner_form").id,
            view_type="form",
        )
        arch = etree.fromstring(view["arch"].encode())

        gender_fields = arch.xpath("//field[@name='gender']")
        dob_fields = arch.xpath("//field[@name='date_of_birth']")
        individual_name_fields = arch.xpath("//field[@name='name' and @invisible='is_company']")

        self.assertEqual(len(gender_fields), 1)
        self.assertEqual(gender_fields[0].get("invisible"), "is_company")
        self.assertEqual(len(dob_fields), 1)
        self.assertEqual(dob_fields[0].get("invisible"), "is_company")
        self.assertEqual(len(individual_name_fields), 1)
        self.assertEqual(
            individual_name_fields[0].get("placeholder"),
            "Last name first, then first name",
        )

    def test_installed_addon_required_tags_contract(self):
        categories = self.env["res.partner.category"]

        for xmlid_name, tag_name in C3_CONTACT_TAGS:
            with self.subTest(tag_name=tag_name):
                tag = self.env.ref(f"{MODULE}.{xmlid_name}")
                self.assertEqual(tag.name, tag_name)
                self.assertEqual(
                    categories.search_count([("name", "=", tag_name)]),
                    1,
                )
